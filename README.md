# CLI Tool

A simple command-line tool for file operations.

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
