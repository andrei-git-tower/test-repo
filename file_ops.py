"""File operations module."""
import os

def read_file(file_path):
    """Read contents from a file."""
    with open(file_path, 'r') as f:
        return f.read()
