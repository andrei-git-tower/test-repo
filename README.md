# CLI Tool

A simple command-line tool for file operations.

## Features

- Read and write files with ease
- Multiple output formats (JSON, CSV, TXT)
- Verbose mode for detailed logging
- Path validation and error handling
- Type-safe operations with type hints
- Comprehensive logging system with colored console output
- Rotating log files to prevent disk space issues

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
- `--log-level`: Set logging level: DEBUG, INFO, WARNING, or ERROR (default: INFO)

## Logging

The CLI tool includes a comprehensive logging system that helps with debugging and monitoring.

### Log Output

- **Console**: Displays INFO-level and above with color-coded severity levels
  - DEBUG: Cyan
  - INFO: Green
  - WARNING: Yellow
  - ERROR: Red
  - CRITICAL: Magenta

- **Files**: Detailed DEBUG-level logs stored in the `logs/` directory
  - Format: `{module_name}_YYYYMMDD.log`
  - Automatic rotation when files reach 10MB
  - Keeps 5 backup files

### Configuration

Configure logging behavior via environment variables:

```bash
export LOG_DIR=/custom/log/path          # Default: logs/
export LOG_MAX_BYTES=20971520            # Default: 10485760 (10MB)
export LOG_BACKUP_COUNT=10               # Default: 5
```

### Example

```bash
# Run with debug logging
python cli.py --log-level DEBUG --verbose input.txt

# Logs will be written to logs/__main___20251212.log
```

## Project Structure

```
.
├── cli.py          # Main CLI entry point
├── config.py       # Configuration settings
├── utils.py        # Utility functions
├── file_ops.py     # File operation functions
└── requirements.txt # Python dependencies
```
