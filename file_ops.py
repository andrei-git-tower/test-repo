"""File operations module."""
import os

def read_file(file_path):
    """Read contents from a file."""
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path, content):
    """Write contents to a file."""
    with open(file_path, 'w') as f:
        f.write(content)
