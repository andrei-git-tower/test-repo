"""File operations module."""
import os
import json
import csv

def read_file(file_path):
    """Read contents from a file."""
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path, content):
    """Write contents to a file."""
    with open(file_path, 'w') as f:
        f.write(content)

def convert_format(data, format_type):
    """Convert data to specified format."""
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'csv':
        return str(data)
    else:
        return str(data)
