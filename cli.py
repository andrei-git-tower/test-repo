#!/usr/bin/env python3
import click
from config import VERSION

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def main(verbose):
    """A simple CLI tool for file operations."""
    if verbose:
        print(f"CLI Tool v{VERSION} (verbose mode)")
    else:
        print(f"CLI Tool v{VERSION}")

if __name__ == "__main__":
    main()
