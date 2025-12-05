#!/usr/bin/env python3
import click
from config import VERSION, APP_NAME
from utils import format_output, validate_path
from file_ops import read_file, write_file

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--output', '-o', default='output.txt', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'txt']), default='txt', help='Output format')
@click.argument('input_file', required=False)
def main(verbose, output, format, input_file):
    """A simple CLI tool for file operations."""
    if verbose:
        print(format_output(f"{APP_NAME} v{VERSION} (verbose mode)"))
        if input_file:
            if validate_path(input_file):
                print(format_output(f"Input file: {input_file}"))
            else:
                print(format_output(f"Warning: Input file not found: {input_file}"))
        print(format_output(f"Output file: {output}"))
        print(format_output(f"Format: {format}"))
    else:
        print(format_output(f"{APP_NAME} v{VERSION}"))

if __name__ == "__main__":
    main()
