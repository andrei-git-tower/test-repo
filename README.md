# CLI Tool

A simple command-line tool for file operations.

## Features

- Read and write files with ease
- Multiple output formats (JSON, CSV, TXT)
- Verbose mode for detailed logging
- Path validation and error handling
- Type-safe operations with type hints

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python cli.py

# With options
python cli.py --verbose --output results.csv --format csv input.txt

# Get help
python cli.py --help
```

### Options

- `-v, --verbose`: Enable verbose output
- `-o, --output`: Specify output file path (default: output.txt)
- `-f, --format`: Choose output format: json, csv, or txt (default: txt)

## Project Structure

```
.
├── cli.py          # Main CLI entry point
├── config.py       # Configuration settings
├── utils.py        # Utility functions
├── file_ops.py     # File operation functions
└── requirements.txt # Python dependencies
```
