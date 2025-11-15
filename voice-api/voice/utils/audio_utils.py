from pydub import AudioSegment
import os
from pathlib import Path
from typing import Optional, Tuple, Dict
import librosa
import numpy as np


def validate_audio_file(file_path: str, max_size_bytes: int = 25 * 1024 * 1024,
                       max_duration_seconds: int = 600,
                       supported_formats: list = None) -> Dict[str, any]:
    """
    Validate audio file format, size, and duration

    Args:
        file_path: Path to the audio file
        max_size_bytes: Maximum allowed file size in bytes (default: 25MB)
        max_duration_seconds: Maximum allowed duration in seconds (default: 600s/10min)
        supported_formats: List of supported file extensions (default: ['webm', 'mp3', 'wav', 'm4a', 'ogg'])

    Returns:
        dict with validation results:
        {
            'valid': bool,
            'errors': list of error messages,
            'warnings': list of warning messages,
            'file_size_bytes': int,
            'duration_seconds': float,
            'format': str
        }
    """
    if supported_formats is None:
        supported_formats = ['webm', 'mp3', 'wav', 'm4a', 'ogg']

    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'file_size_bytes': 0,
        'duration_seconds': 0.0,
        'format': ''
    }

    # Check if file exists
    if not os.path.exists(file_path):
        result['valid'] = False
        result['errors'].append(f"File not found: {file_path}")
        return result

    # Check file size
    try:
        file_size = os.path.getsize(file_path)
        result['file_size_bytes'] = file_size

        if file_size > max_size_bytes:
            result['valid'] = False
            result['errors'].append(
                f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds "
                f"maximum allowed size ({max_size_bytes / 1024 / 1024:.2f}MB)"
            )
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"Error checking file size: {str(e)}")
        return result

    # Check file format
    file_ext = Path(file_path).suffix.lower().lstrip('.')
    result['format'] = file_ext

    if file_ext not in supported_formats:
        result['valid'] = False
        result['errors'].append(
            f"Unsupported format '{file_ext}'. "
            f"Supported formats: {', '.join(supported_formats)}"
        )

    # Check duration
    try:
        duration = get_audio_duration(file_path)
        result['duration_seconds'] = duration

        if duration > max_duration_seconds:
            result['valid'] = False
            result['errors'].append(
                f"Audio duration ({duration:.2f}s) exceeds "
                f"maximum allowed duration ({max_duration_seconds}s)"
            )

        if duration < 0.1:
            result['warnings'].append("Audio duration is very short (< 0.1s)")

    except Exception as e:
        result['warnings'].append(f"Could not determine audio duration: {str(e)}")

    return result


def convert_audio_format(input_path: str, output_format: str = "wav",
                        output_path: Optional[str] = None) -> str:
    """
    Convert audio file to specified format using pydub

    Args:
        input_path: Path to input audio file
        output_format: Desired output format (default: 'wav')
        output_path: Optional custom output path. If not provided, will use input filename with new extension

    Returns:
        str: Path to converted audio file

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If conversion fails
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        # Load audio file
        audio = AudioSegment.from_file(input_path)

        # Determine output path
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(input_file.parent / f"{input_file.stem}.{output_format}")

        # Export to new format
        audio.export(output_path, format=output_format)

        return output_path

    except Exception as e:
        raise ValueError(f"Error converting audio format: {str(e)}")


def get_audio_duration(file_path: str) -> float:
    """
    Get duration of audio file in seconds

    Args:
        file_path: Path to audio file

    Returns:
        float: Duration in seconds

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If duration cannot be determined
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    try:
        # Try using pydub first (faster for most formats)
        audio = AudioSegment.from_file(file_path)
        duration = len(audio) / 1000.0  # pydub returns duration in milliseconds
        return duration

    except Exception as e:
        # Fallback to librosa
        try:
            y, sr = librosa.load(file_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            return duration
        except Exception as e2:
            raise ValueError(f"Could not determine audio duration: {str(e2)}")


def compress_audio(file_path: str, target_bitrate: str = "128k",
                  output_path: Optional[str] = None) -> str:
    """
    Compress audio file to reduce size

    Args:
        file_path: Path to input audio file
        target_bitrate: Target bitrate (e.g., '128k', '64k', '192k')
        output_path: Optional custom output path

    Returns:
        str: Path to compressed audio file

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If compression fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        # Load audio file
        audio = AudioSegment.from_file(file_path)

        # Determine output path
        if output_path is None:
            input_file = Path(file_path)
            output_path = str(input_file.parent / f"{input_file.stem}_compressed{input_file.suffix}")

        # Export with specified bitrate
        audio.export(
            output_path,
            format=Path(file_path).suffix.lstrip('.'),
            bitrate=target_bitrate
        )

        return output_path

    except Exception as e:
        raise ValueError(f"Error compressing audio: {str(e)}")


def normalize_audio(file_path: str, target_dBFS: float = -20.0,
                   output_path: Optional[str] = None) -> str:
    """
    Normalize audio levels

    Args:
        file_path: Path to input audio file
        target_dBFS: Target loudness in dBFS (default: -20.0)
        output_path: Optional custom output path

    Returns:
        str: Path to normalized audio file

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If normalization fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        # Load audio file
        audio = AudioSegment.from_file(file_path)

        # Calculate change needed to reach target dBFS
        change_in_dBFS = target_dBFS - audio.dBFS

        # Apply normalization
        normalized_audio = audio.apply_gain(change_in_dBFS)

        # Determine output path
        if output_path is None:
            input_file = Path(file_path)
            output_path = str(input_file.parent / f"{input_file.stem}_normalized{input_file.suffix}")

        # Export normalized audio
        normalized_audio.export(
            output_path,
            format=Path(file_path).suffix.lstrip('.')
        )

        return output_path

    except Exception as e:
        raise ValueError(f"Error normalizing audio: {str(e)}")


def get_audio_info(file_path: str) -> Dict[str, any]:
    """
    Get comprehensive information about an audio file

    Args:
        file_path: Path to audio file

    Returns:
        dict with audio information including:
        - duration_seconds
        - sample_rate
        - channels
        - file_size_bytes
        - format
        - bitrate (if available)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    info = {}

    try:
        # Get basic file info
        info['file_size_bytes'] = os.path.getsize(file_path)
        info['format'] = Path(file_path).suffix.lower().lstrip('.')

        # Use pydub for basic audio properties
        audio = AudioSegment.from_file(file_path)
        info['duration_seconds'] = len(audio) / 1000.0
        info['channels'] = audio.channels
        info['sample_rate'] = audio.frame_rate
        info['sample_width'] = audio.sample_width

        # Calculate bitrate
        if info['duration_seconds'] > 0:
            info['bitrate_kbps'] = (info['file_size_bytes'] * 8) / (info['duration_seconds'] * 1000)

    except Exception as e:
        info['error'] = f"Could not extract audio info: {str(e)}"

    return info
