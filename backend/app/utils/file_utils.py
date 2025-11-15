"""
File handling utilities for uploads and downloads.
"""
import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.core.logging import logger


def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    """
    Generate a unique filename with UUID to prevent collisions.
    
    Args:
        original_filename: Original name of the uploaded file
        prefix: Optional prefix for the filename
    
    Returns:
        str: Unique filename
    """
    file_extension = Path(original_filename).suffix
    unique_id = str(uuid.uuid4())
    
    if prefix:
        return f"{prefix}_{unique_id}{file_extension}"
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


async def save_upload_file(
    file: UploadFile,
    subdirectory: str,
    prefix: str = ""
) -> Tuple[str, str]:
    """
    Save uploaded file to storage.
    
    Args:
        file: FastAPI UploadFile object
        subdirectory: Subdirectory within uploads folder (e.g., 'resumes', 'audio')
        prefix: Optional prefix for filename
    
    Returns:
        tuple: (file_path, unique_filename)
    
    Raises:
        HTTPException: If file validation fails or save fails
    """
    # Validate file type
    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {settings.allowed_file_types_list}"
        )
    
    # Read file content to check size
    content = await file.read()
    if not validate_file_size(len(content)):
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds limit of {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename, prefix)
    
    # Create full path
    upload_dir = Path(settings.UPLOAD_DIR) / subdirectory
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        logger.info(f"File saved successfully: {file_path}")
        return str(file_path), unique_filename
    except Exception as e:
        logger.error(f"Error saving file: {e}")
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
