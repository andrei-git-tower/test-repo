"""File operations module."""
import os
import json
import csv
from typing import Any

def read_file(file_path: str) -> str:
    """Read contents from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path: str, content: str) -> None:
    """Write contents to a file."""
    with open(file_path, 'w') as f:
        f.write(content)

def convert_format(data: Any, format_type: str) -> str:
    """Convert data to specified format."""
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'csv':
        return str(data)
    else:
        return str(data)
