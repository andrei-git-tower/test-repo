"""Utility functions for the CLI tool."""
import os
from typing import Optional

def format_output(text: Optional[str]) -> str:
    """Format text for output with proper escaping."""
    if text is None:
        return "[OUTPUT] (empty)"
    return f"[OUTPUT] {text}"

def validate_path(path: str) -> bool:
    """Validate file path."""
    return os.path.exists(path)

def get_file_extension(path: str) -> str:
    """Get file extension from path."""
    return os.path.splitext(path)[1]
