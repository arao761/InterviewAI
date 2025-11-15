"""
Transcription Service
Handles advanced audio transcription with Whisper API
Includes chunking, retry logic, and multiple response formats
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from io import BytesIO
import tempfile

from openai import OpenAI
from pydub import AudioSegment

from config import Config
from utils.audio_utils import (
    get_audio_duration,
    convert_audio_format,
    get_audio_info,
    validate_audio_file
)


class TranscriptionService:
    """
    Advanced transcription service with chunking, retry logic, and multiple formats
    """

    # Whisper API limits
    MAX_FILE_SIZE_MB = 25
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    CHUNK_DURATION_SECONDS = 300  # 5 minutes per chunk (safe margin under 25MB limit)

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize transcription service

        Args:
            api_key: OpenAI API key (uses Config if not provided)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    def transcribe(
        self,
        audio_data: bytes,
        filename: str,
        language: Optional[str] = "en",
        response_format: str = "verbose_json",
        include_timestamps: bool = True,
        include_confidence: bool = True,
        chunk_large_files: bool = True,
    ) -> Dict:
        """
        Transcribe audio with advanced features

        Args:
            audio_data: Audio file bytes
            filename: Original filename
            language: Language code (default: "en" for English)
            response_format: Response format ("text", "json", "verbose_json", "srt", "vtt")
            include_timestamps: Include word-level timestamps
            include_confidence: Include confidence scores (requires verbose_json)
            chunk_large_files: Automatically chunk files larger than 25MB

        Returns:
            Dict with transcription results
        """
        file_size = len(audio_data)

        # Validate file size
        if file_size > Config.MAX_AUDIO_SIZE_BYTES and not chunk_large_files:
            raise ValueError(
                f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds maximum "
                f"({Config.MAX_AUDIO_SIZE_MB}MB). Enable chunk_large_files to process."
            )

        # Save to temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
            temp_path = temp_file.name
            temp_file.write(audio_data)

        try:
            # Get audio info (may fail for some formats, that's OK)
            try:
                audio_info = get_audio_info(temp_path)
            except Exception as e:
                # If we can't get audio info, use defaults
                audio_info = {
                    'duration_seconds': 0,
                    'format': Path(filename).suffix.lower().lstrip('.') or 'unknown',
                    'sample_rate': 0,
                    'channels': 0
                }
            duration = audio_info.get('duration_seconds', 0)

            # Check if file needs chunking
            if chunk_large_files and file_size > self.MAX_FILE_SIZE_BYTES:
                return self._transcribe_chunked(
                    temp_path,
                    filename,
                    language,
                    response_format,
                    include_timestamps,
                    include_confidence,
                    audio_info
                )

            # Process single file
            return self._transcribe_single(
                temp_path,
                filename,
                language,
                response_format,
                include_timestamps,
                include_confidence,
                audio_info
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def _transcribe_single(
        self,
        file_path: str,
        filename: str,
        language: Optional[str],
        response_format: str,
        include_timestamps: bool,
        include_confidence: bool,
        audio_info: Dict
    ) -> Dict:
        """
        Transcribe a single audio file
        """
        # Convert to format compatible with Whisper if needed
        processed_path = self._prepare_audio_file(file_path, filename)

        try:
            # Prepare Whisper API parameters
            whisper_format = "verbose_json" if (include_timestamps or include_confidence) else response_format

            # Read processed file
            with open(processed_path, 'rb') as audio_file:
                # Call Whisper API with retry logic
                transcript_response = self._call_whisper_with_retry(
                    audio_file,
                    filename,
                    language,
                    whisper_format
                )

            # Process response
            result = self._process_whisper_response(
                transcript_response,
                response_format,
                include_timestamps,
                include_confidence,
                audio_info
            )

            return result

        finally:
            # Clean up processed file if different from original
            if processed_path != file_path and os.path.exists(processed_path):
                os.unlink(processed_path)

    def _transcribe_chunked(
        self,
        file_path: str,
        filename: str,
        language: Optional[str],
        response_format: str,
        include_timestamps: bool,
        include_confidence: bool,
        audio_info: Dict
    ) -> Dict:
        """
        Transcribe large audio file by splitting into chunks
        """
        audio = AudioSegment.from_file(file_path)
        duration_ms = len(audio)
        chunk_duration_ms = self.CHUNK_DURATION_SECONDS * 1000

        chunks = []
        transcripts = []

        # Split audio into chunks
        for start_ms in range(0, duration_ms, chunk_duration_ms):
            end_ms = min(start_ms + chunk_duration_ms, duration_ms)
            chunk = audio[start_ms:end_ms]

            # Save chunk to temporary file
            chunk_path = f"{file_path}_chunk_{len(chunks)}.wav"
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)

        try:
            # Transcribe each chunk
            for i, chunk_path in enumerate(chunks):
                chunk_info = get_audio_info(chunk_path)
                
                with open(chunk_path, 'rb') as chunk_file:
                    chunk_response = self._call_whisper_with_retry(
                        chunk_file,
                        f"{filename}_chunk_{i}",
                        language,
                        "verbose_json"
                    )

                # Process chunk response
                chunk_result = self._process_whisper_response(
                    chunk_response,
                    "verbose_json",
                    include_timestamps,
                    include_confidence,
                    chunk_info
                )

                transcripts.append(chunk_result)

            # Merge transcripts
            return self._merge_transcripts(
                transcripts,
                response_format,
                include_timestamps,
                include_confidence,
                audio_info
            )

        finally:
            # Clean up chunk files
            for chunk_path in chunks:
                if os.path.exists(chunk_path):
                    os.unlink(chunk_path)

    def _prepare_audio_file(self, file_path: str, filename: str) -> str:
        """
        Prepare audio file for Whisper API
        Converts to compatible format if needed
        """
        file_ext = Path(filename).suffix.lower().lstrip('.')

        # Whisper supports: mp3, mp4, mpeg, mpga, m4a, wav, webm
        whisper_formats = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

        if file_ext in whisper_formats:
            return file_path

        # Convert to WAV if format not directly supported
        try:
            converted_path = convert_audio_format(file_path, "wav")
            return converted_path
        except Exception as e:
            # If conversion fails, try original format (Whisper might still accept it)
            return file_path

    def _call_whisper_with_retry(
        self,
        audio_file,
        filename: str,
        language: Optional[str],
        response_format: str
    ):
        """
        Call Whisper API with retry logic
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                # Reset file pointer
                audio_file.seek(0)
                
                params = {
                    "model": Config.WHISPER_MODEL,
                    "file": (filename, audio_file, f"audio/{Path(filename).suffix.lstrip('.') or 'mpeg'}"),
                    "response_format": response_format,
                }

                # Add language if specified
                if language:
                    params["language"] = language

                # Call API
                response = self.client.audio.transcriptions.create(**params)
                return response

            except Exception as e:
                last_error = e
                error_msg = str(e).lower()

                # Don't retry on certain errors
                if "invalid api key" in error_msg or "authentication" in error_msg:
                    raise

                # Rate limit - wait longer
                if "rate limit" in error_msg:
                    wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    time.sleep(wait_time)
                    continue

                # Other errors - retry with delay
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue

        # All retries failed
        raise Exception(f"Transcription failed after {self.max_retries} attempts: {str(last_error)}")

    def _process_whisper_response(
        self,
        response,
        response_format: str,
        include_timestamps: bool,
        include_confidence: bool,
        audio_info: Dict
    ) -> Dict:
        """
        Process Whisper API response into standardized format
        """
        # Handle different response formats
        response_duration = None
        if isinstance(response, str):
            # Plain text response
            transcript_text = response
            words = []
            segments = []
        elif hasattr(response, 'text'):
            # Verbose JSON response object
            transcript_text = response.text
            words = getattr(response, 'words', []) if include_timestamps else []
            segments = getattr(response, 'segments', []) if include_timestamps else []
            # Try to get duration from response
            response_duration = getattr(response, 'duration', None)
        elif isinstance(response, dict):
            # JSON dict response
            transcript_text = response.get('text', '')
            words = response.get('words', []) if include_timestamps else []
            segments = response.get('segments', []) if include_timestamps else []
            response_duration = response.get('duration', None)
        else:
            transcript_text = str(response)
            words = []
            segments = []

        # Calculate duration from segments if not available
        if response_duration is None and segments:
            if isinstance(segments, list) and len(segments) > 0:
                # Get duration from last segment
                last_segment = segments[-1]
                if isinstance(last_segment, dict):
                    response_duration = last_segment.get('end', 0)
                else:
                    response_duration = getattr(last_segment, 'end', 0)

        # Use response duration if available, otherwise fall back to audio_info
        duration = response_duration if response_duration is not None else audio_info.get('duration_seconds', 0)

        # Build result
        result = {
            "status": "success",
            "transcript": transcript_text,
            "metadata": {
                "duration_seconds": duration,
                "format": audio_info.get('format', 'unknown'),
                "sample_rate": audio_info.get('sample_rate', 0) or None,
                "channels": audio_info.get('channels', 0) or None,
                "model": Config.WHISPER_MODEL,
            }
        }

        # Add timestamps if requested
        if include_timestamps and (words or segments):
            result["timestamps"] = {
                "words": self._format_words(words) if words else [],
                "segments": self._format_segments(segments) if segments else []
            }

        # Add confidence scores if requested
        if include_confidence:
            confidence_data = self._extract_confidence_scores(words, segments)
            if confidence_data:
                result["confidence"] = confidence_data
            else:
                # Return structure even if no confidence data available
                # This ensures the API always returns confidence structure when requested
                result["confidence"] = {
                    "average": None,
                    "word_level": [],
                    "note": "Confidence scores not available from Whisper API. Whisper API does not provide confidence scores directly."
                }

        return result

    def _format_words(self, words: List) -> List[Dict]:
        """
        Format word-level timestamps
        Handles both dict and object responses from OpenAI
        """
        formatted = []
        for word in words:
            # Handle both dict and object responses
            if isinstance(word, dict):
                word_text = word.get('word', '')
                word_start = word.get('start', 0)
                word_end = word.get('end', 0)
            else:
                # Object response (TranscriptionWord)
                word_text = getattr(word, 'word', '')
                word_start = getattr(word, 'start', 0)
                word_end = getattr(word, 'end', 0)
            
            formatted.append({
                "word": word_text,
                "start": word_start,
                "end": word_end,
            })
        return formatted

    def _format_segments(self, segments: List) -> List[Dict]:
        """
        Format segment-level timestamps
        Handles both dict and object responses from OpenAI
        """
        formatted = []
        for segment in segments:
            # Handle both dict and object responses
            if isinstance(segment, dict):
                segment_text = segment.get('text', '').strip()
                segment_start = segment.get('start', 0)
                segment_end = segment.get('end', 0)
            else:
                # Object response (TranscriptionSegment)
                segment_text = getattr(segment, 'text', '').strip()
                segment_start = getattr(segment, 'start', 0)
                segment_end = getattr(segment, 'end', 0)
            
            formatted.append({
                "text": segment_text,
                "start": segment_start,
                "end": segment_end,
            })
        return formatted

    def _format_words_with_confidence(self, words: List) -> List[Dict]:
        """
        Format words with confidence scores
        Handles both dict and object responses from OpenAI
        Tries multiple possible confidence field names
        """
        formatted = []
        for word in words:
            # Handle both dict and object responses
            if isinstance(word, dict):
                word_text = word.get('word', '')
                word_start = word.get('start', 0)
                word_end = word.get('end', 0)
                # Try multiple possible confidence field names
                word_confidence = (
                    word.get('probability') or 
                    word.get('confidence') or 
                    word.get('logprob') or
                    None
                )
            else:
                # Object response (TranscriptionWord)
                word_text = getattr(word, 'word', '')
                word_start = getattr(word, 'start', 0)
                word_end = getattr(word, 'end', 0)
                # Try multiple possible confidence attributes
                word_confidence = (
                    getattr(word, 'probability', None) or
                    getattr(word, 'confidence', None) or
                    getattr(word, 'logprob', None) or
                    None
                )
            
            formatted.append({
                "word": word_text,
                "start": word_start,
                "end": word_end,
                "confidence": word_confidence,
            })
        return formatted

    def _extract_confidence_scores(self, words: List, segments: List) -> Optional[Dict]:
        """
        Extract confidence scores from words and segments
        Returns confidence data if available, None otherwise
        """
        if not words:
            return None

        # Try to extract confidence/probability from words
        word_confidences = []
        word_level_data = []
        
        for word in words:
            # Handle both dict and object responses
            if isinstance(word, dict):
                word_text = word.get('word', '')
                word_start = word.get('start', 0)
                word_end = word.get('end', 0)
                # Try multiple possible confidence field names
                confidence = (
                    word.get('probability') or 
                    word.get('confidence') or 
                    word.get('logprob') or
                    None
                )
            else:
                # Object response (TranscriptionWord)
                word_text = getattr(word, 'word', '')
                word_start = getattr(word, 'start', 0)
                word_end = getattr(word, 'end', 0)
                # Try multiple possible confidence attributes
                confidence = (
                    getattr(word, 'probability', None) or
                    getattr(word, 'confidence', None) or
                    getattr(word, 'logprob', None) or
                    None
                )
            
            if confidence is not None:
                word_confidences.append(confidence)
                word_level_data.append({
                    "word": word_text,
                    "start": word_start,
                    "end": word_end,
                    "confidence": confidence
                })
            else:
                # Include word even without confidence
                word_level_data.append({
                    "word": word_text,
                    "start": word_start,
                    "end": word_end,
                    "confidence": None
                })

        # Calculate average if we have any confidence scores
        if word_confidences:
            avg_confidence = sum(word_confidences) / len(word_confidences)
            return {
                "average": avg_confidence,
                "word_level": word_level_data,
                "words_with_confidence": len(word_confidences),
                "total_words": len(word_level_data)
            }
        
        # No confidence scores found
        return None

    def _calculate_average_confidence(self, words: List) -> Optional[float]:
        """
        Calculate average confidence score from words
        Handles both dict and object responses from OpenAI
        Returns None if no confidence scores available
        """
        if not words:
            return None

        confidences = []
        for word in words:
            # Handle both dict and object responses
            if isinstance(word, dict):
                # Try multiple possible confidence field names
                prob = (
                    word.get('probability') or 
                    word.get('confidence') or 
                    word.get('logprob') or
                    None
                )
            else:
                # Object response (TranscriptionWord)
                prob = (
                    getattr(word, 'probability', None) or
                    getattr(word, 'confidence', None) or
                    getattr(word, 'logprob', None) or
                    None
                )
            
            if prob is not None:
                confidences.append(prob)

        if not confidences:
            return None

        return sum(confidences) / len(confidences)

    def _merge_transcripts(
        self,
        transcripts: List[Dict],
        response_format: str,
        include_timestamps: bool,
        include_confidence: bool,
        audio_info: Dict
    ) -> Dict:
        """
        Merge multiple chunk transcripts into one
        """
        # Combine transcript texts
        full_text = " ".join([t.get("transcript", "") for t in transcripts])

        # Combine timestamps with offset
        all_words = []
        all_segments = []
        time_offset = 0

        for transcript in transcripts:
            if include_timestamps and "timestamps" in transcript:
                words = transcript["timestamps"].get("words", [])
                segments = transcript["timestamps"].get("segments", [])

                # Adjust timestamps with offset
                for word in words:
                    word["start"] += time_offset
                    word["end"] += time_offset
                    all_words.append(word)

                for segment in segments:
                    segment["start"] += time_offset
                    segment["end"] += time_offset
                    all_segments.append(segment)

                # Update offset for next chunk
                if segments:
                    time_offset = segments[-1].get("end", time_offset)

        # Build merged result
        result = {
            "status": "success",
            "transcript": full_text,
            "metadata": {
                **audio_info,
                "model": Config.WHISPER_MODEL,
                "chunked": True,
                "num_chunks": len(transcripts),
            }
        }

        if include_timestamps:
            result["timestamps"] = {
                "words": all_words,
                "segments": all_segments
            }

        if include_confidence:
            all_confidences = []
            for transcript in transcripts:
                if "confidence" in transcript and "word_level" in transcript["confidence"]:
                    all_confidences.extend(transcript["confidence"]["word_level"])

            if all_confidences:
                # Filter out None confidence values
                confidences_with_values = [w.get("confidence") for w in all_confidences if w.get("confidence") is not None]
                
                if confidences_with_values:
                    avg_confidence = sum(confidences_with_values) / len(confidences_with_values)
                    result["confidence"] = {
                        "average": avg_confidence,
                        "word_level": all_confidences,
                        "words_with_confidence": len(confidences_with_values),
                        "total_words": len(all_confidences)
                    }
                else:
                    # No confidence values available
                    result["confidence"] = {
                        "average": None,
                        "word_level": all_confidences,
                        "note": "Confidence scores not available from Whisper API"
                    }
            else:
                # No confidence data at all
                result["confidence"] = {
                    "average": None,
                    "word_level": [],
                    "note": "Confidence scores not available from Whisper API. Whisper API does not provide confidence scores directly."
                }

        return result

