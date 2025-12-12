#!/usr/bin/env python3
import click
from config import VERSION

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--output', '-o', default='output.txt', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'txt']), default='txt', help='Output format')
@click.argument('input_file', required=False)
def main(verbose, output, format, input_file):
    """A simple CLI tool for file operations."""
    if verbose:
        print(f"CLI Tool v{VERSION} (verbose mode)")
        if input_file:
            print(f"Input file: {input_file}")
        print(f"Output file: {output}")
        print(f"Format: {format}")
    else:
        print(f"CLI Tool v{VERSION}")

if __name__ == "__main__":
    main()
