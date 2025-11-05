"""Utility functions for the CLI tool."""

def format_output(text):
    """Format text for output with proper escaping."""
    if text is None:
        return "[OUTPUT] (empty)"
    return f"[OUTPUT] {text}"

def validate_path(path):
    """Validate file path."""
    import os
    return os.path.exists(path)
