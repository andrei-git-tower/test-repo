"""Caching utilities for performance optimization."""
from functools import lru_cache
from typing import Optional

@lru_cache(maxsize=128)
def cached_file_read(file_path: str) -> Optional[str]:
    """Read file with caching for better performance."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
