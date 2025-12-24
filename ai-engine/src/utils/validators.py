"""
Validators
Utility functions for data validation and sanitization
"""

import re
from pathlib import Path
from typing import Optional, List


def validate_file_path(file_path: str, allowed_extensions: Optional[List[str]] = None) -> Path:
    """
    Validate file path exists and has allowed extension

    Args:
        file_path: Path to file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.docx'])

    Returns:
        Path object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If extension not allowed
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if allowed_extensions:
        if path.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
            raise ValueError(
                f"Invalid file extension: {path.suffix}. "
                f"Allowed: {', '.join(allowed_extensions)}"
            )

    return path


def validate_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email address

    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL string

    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False

    pattern = r'^https?://[^\s]+$'
    return bool(re.match(pattern, url))


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text by removing excessive whitespace and special characters

    Args:
        text: Input text
        max_length: Maximum length (optional)

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove null bytes and control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length] + "..."

    return text


def validate_domain(domain: str, allowed_domains: List[str]) -> bool:
    """
    Validate domain is in allowed list

    Args:
        domain: Domain string
        allowed_domains: List of allowed domains

    Returns:
        True if valid, False otherwise
    """
    return domain.lower() in [d.lower() for d in allowed_domains]


def validate_score(score: int, min_score: int = 0, max_score: int = 100) -> bool:
    """
    Validate score is within valid range

    Args:
        score: Score value
        min_score: Minimum allowed score
        max_score: Maximum allowed score

    Returns:
        True if valid, False otherwise
    """
    return min_score <= score <= max_score


def extract_years_of_experience(text: str) -> Optional[float]:
    """
    Extract years of experience from text

    Args:
        text: Text containing experience duration

    Returns:
        Years as float, or None if not found
    """
    # Patterns like "2 years", "3-5 years", "6 months"
    year_pattern = r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)'
    month_pattern = r'(\d+)\s*(?:months?|mos?)'

    years = 0.0

    # Find years
    year_matches = re.findall(year_pattern, text, re.IGNORECASE)
    if year_matches:
        years += float(year_matches[0])

    # Find months and convert to years
    month_matches = re.findall(month_pattern, text, re.IGNORECASE)
    if month_matches:
        years += float(month_matches[0]) / 12

    return years if years > 0 else None


def validate_transcript_length(
    transcript: str,
    min_length: int = 50,
    max_length: int = 10000
) -> tuple[bool, Optional[str]]:
    """
    Validate transcript length is appropriate

    Args:
        transcript: Interview transcript
        min_length: Minimum character length
        max_length: Maximum character length

    Returns:
        Tuple of (is_valid, error_message)
    """
    length = len(transcript.strip())

    if length < min_length:
        return False, f"Transcript too short ({length} chars). Minimum: {min_length}"

    if length > max_length:
        return False, f"Transcript too long ({length} chars). Maximum: {max_length}"

    return True, None
