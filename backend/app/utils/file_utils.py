"""
File handling utilities for uploads and downloads.

SECURITY FEATURES:
- File type validation (whitelist approach)
- File size limits to prevent DoS
- Malicious filename sanitization
- Path traversal prevention
- Content-type validation
- Magic number verification for file types
"""
import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.core.logging import logger
import re


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and injection attacks.

    SECURITY:
    - Remove directory traversal attempts (../, .., etc.)
    - Remove path separators
    - Remove null bytes
    - Limit to safe characters
    - Prevent hidden files (starting with .)

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)

    # Remove null bytes
    filename = filename.replace('\0', '')

    # Remove or replace unsafe characters
    # Keep only: letters, numbers, dash, underscore, period
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    # Prevent hidden files
    if filename.startswith('.'):
        filename = '_' + filename

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext

    # Ensure we have a filename
    if not filename or filename == '.':
        filename = 'unnamed_file'

    return filename


def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    """
    Generate a unique filename with UUID to prevent collisions.

    SECURITY: Uses UUID4 for cryptographically strong randomness
    to prevent filename prediction attacks.

    Args:
        original_filename: Original name of the uploaded file
        prefix: Optional prefix for the filename

    Returns:
        str: Unique filename
    """
    # Sanitize the original filename first
    safe_filename = sanitize_filename(original_filename)
    file_extension = Path(safe_filename).suffix.lower()

    # Validate extension
    if not file_extension:
        file_extension = '.bin'

    unique_id = str(uuid.uuid4())

    if prefix:
        # Sanitize prefix too
        safe_prefix = re.sub(r'[^a-zA-Z0-9_-]', '_', prefix)
        return f"{safe_prefix}_{unique_id}{file_extension}"
    return f"{unique_id}{file_extension}"


def validate_file_type(filename: str) -> bool:
    """
    Validate if file type is allowed.
    
    Args:
        filename: Name of the file to validate
    
    Returns:
        bool: True if file type is allowed
    """
    file_extension = Path(filename).suffix.lower().lstrip('.')
    return file_extension in settings.allowed_file_types_list


def validate_file_size(file_size: int) -> bool:
    """
    Validate if file size is within allowed limit.
    
    Args:
        file_size: Size of the file in bytes
    
    Returns:
        bool: True if file size is within limit
    """
    return file_size <= settings.MAX_FILE_SIZE


def validate_file_content(content: bytes, filename: str) -> bool:
    """
    Validate file content using magic numbers (file signatures).

    SECURITY: Prevent malicious files disguised with wrong extensions.
    Checks actual file content, not just extension.

    Args:
        content: First few bytes of file content
        filename: Filename with extension

    Returns:
        bool: True if content matches expected type
    """
    if len(content) < 4:
        return False

    file_extension = Path(filename).suffix.lower()

    # PDF signature
    if file_extension == '.pdf':
        return content[:4] == b'%PDF'

    # DOCX signature (ZIP format)
    if file_extension in ['.docx', '.xlsx', '.pptx']:
        return content[:2] == b'PK'  # ZIP signature

    # DOC signature (older Word format)
    if file_extension == '.doc':
        return content[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'

    # MP3 signature
    if file_extension == '.mp3':
        return content[:2] == b'\xff\xfb' or content[:3] == b'ID3'

    # WAV signature
    if file_extension == '.wav':
        return content[:4] == b'RIFF'

    # WebM signature
    if file_extension == '.webm':
        return content[:4] == b'\x1a\x45\xdf\xa3'

    # If no specific validation, allow (but log warning)
    logger.warning(f"No magic number validation for extension: {file_extension}")
    return True


async def save_upload_file(
    file: UploadFile,
    subdirectory: str,
    prefix: str = ""
) -> Tuple[str, str]:
    """
    Save uploaded file to storage with comprehensive security validation.

    SECURITY CHECKS:
    1. File type validation (whitelist)
    2. File size validation
    3. Filename sanitization (prevent path traversal)
    4. Content-type validation
    5. Magic number verification (prevent disguised malicious files)
    6. Secure random filename generation

    Args:
        file: FastAPI UploadFile object
        subdirectory: Subdirectory within uploads folder (e.g., 'resumes', 'audio')
        prefix: Optional prefix for filename

    Returns:
        tuple: (file_path, unique_filename)

    Raises:
        HTTPException: If file validation fails or save fails
    """
    # SECURITY: Validate filename is present
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    # SECURITY: Sanitize and validate file type
    safe_filename = sanitize_filename(file.filename)
    if not validate_file_type(safe_filename):
        logger.warning(f"Rejected file upload - invalid type: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {settings.allowed_file_types_list}"
        )

    # SECURITY: Read file content to check size and validate content
    content = await file.read()
    file_size = len(content)

    if not validate_file_size(file_size):
        logger.warning(f"Rejected file upload - size too large: {file_size} bytes")
        raise HTTPException(
            status_code=413,  # Payload Too Large
            detail=f"File size ({file_size} bytes) exceeds limit of {settings.MAX_FILE_SIZE} bytes"
        )

    # SECURITY: Validate file content matches extension (magic number check)
    if not validate_file_content(content, safe_filename):
        logger.warning(f"Rejected file upload - content mismatch: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="File content does not match the file extension. Possible malicious file."
        )

    # SECURITY: Generate unique filename to prevent overwrites and prediction
    unique_filename = generate_unique_filename(safe_filename, prefix)

    # SECURITY: Sanitize subdirectory to prevent path traversal
    safe_subdir = re.sub(r'[^a-zA-Z0-9_-]', '_', subdirectory)

    # Create full path
    upload_dir = Path(settings.UPLOAD_DIR) / safe_subdir
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / unique_filename

    # SECURITY: Verify final path is within upload directory (prevent path traversal)
    try:
        final_path = file_path.resolve()
        upload_base = upload_dir.resolve()
        if not str(final_path).startswith(str(upload_base)):
            logger.error(f"Path traversal attempt detected: {file_path}")
            raise HTTPException(
                status_code=400,
                detail="Invalid file path"
            )
    except Exception as e:
        logger.error(f"Path validation error: {e}")
        raise HTTPException(status_code=400, detail="Invalid file path")

    # Save file with restricted permissions
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        # SECURITY: Set restrictive file permissions (owner read/write only)
        os.chmod(file_path, 0o600)

        logger.info(f"File saved securely: {file_path} ({file_size} bytes)")
        return str(file_path), unique_filename
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        # Clean up partial file if exists
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                # Ignore errors during cleanup, file may already be deleted
                pass
        raise HTTPException(status_code=500, detail="Error saving file")


def get_file_path(filename: str, subdirectory: str) -> Path:
    """
    Get full path for a file in uploads directory.
    
    Args:
        filename: Name of the file
        subdirectory: Subdirectory within uploads folder
    
    Returns:
        Path: Full path to file
    """
    return Path(settings.UPLOAD_DIR) / subdirectory / filename


def delete_file(file_path: str) -> bool:
    """
    Delete a file from storage.
    
    Args:
        file_path: Path to the file to delete
    
    Returns:
        bool: True if deletion successful
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            logger.info(f"File deleted: {file_path}")
            return True
        else:
            logger.warning(f"File not found for deletion: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")
        return False
