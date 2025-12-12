#!/usr/bin/env python3
import click
from config import VERSION, APP_NAME
from utils import format_output, validate_path
from file_ops import read_file, write_file
from logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--output', '-o', default='output.txt', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'txt']), default='txt', help='Output format')
@click.option('--log-level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), help='Set logging level')
@click.argument('input_file', required=False)
def main(verbose, output, format, log_level, input_file):
    """A simple CLI tool for file operations."""
    logger.info(f"Starting {APP_NAME} v{VERSION}")
    logger.debug(f"Log level set to: {log_level}")

    if verbose:
        logger.setLevel(log_level)
        print(format_output(f"{APP_NAME} v{VERSION} (verbose mode)"))
        logger.info("Verbose mode enabled")

        if input_file:
            if validate_path(input_file):
                print(format_output(f"Input file: {input_file}"))
                logger.info(f"Valid input file provided: {input_file}")
            else:
                print(format_output(f"Warning: Input file not found: {input_file}"))
                logger.warning(f"Input file not found: {input_file}")

        print(format_output(f"Output file: {output}"))
        print(format_output(f"Format: {format}"))
        logger.debug(f"Output configuration - file: {output}, format: {format}")
    else:
        print(format_output(f"{APP_NAME} v{VERSION}"))

    logger.info("CLI execution completed successfully")

if __name__ == "__main__":
    main()
