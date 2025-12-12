"""
Configuration settings with support for config file loading.

This module provides configuration management with the following priority:
1. Command-line arguments (highest priority)
2. Configuration file (.cli-tool.yaml or .cli-tool.json)
3. Environment variables
4. Default values (lowest priority)
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration values
VERSION = "0.2.1"
DEFAULT_TIMEOUT = 30
APP_NAME = "CLI Tool"

# Performance settings
ENABLE_CACHE = True
CACHE_SIZE = 128
MAX_FILE_SIZE = 1024 * 1024  # 1MB

# Logging defaults
DEFAULT_LOG_LEVEL = "INFO"

# Configuration file names (searched in order)
CONFIG_FILE_NAMES = ['.cli-tool.yaml', '.cli-tool.yml', '.cli-tool.json']


class ConfigLoader:
    """Load and merge configuration from multiple sources."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Optional explicit path to config file
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_defaults()

    def _load_defaults(self):
        """Load default configuration values."""
        self._config = {
            'version': VERSION,
            'app_name': APP_NAME,
            'timeout': DEFAULT_TIMEOUT,
            'enable_cache': ENABLE_CACHE,
            'cache_size': CACHE_SIZE,
            'max_file_size': MAX_FILE_SIZE,
            'log_level': DEFAULT_LOG_LEVEL,
        }

    def _find_config_file(self) -> Optional[Path]:
        """
        Search for configuration file in current directory and parent directories.

        Returns:
            Path to config file if found, None otherwise
        """
        if self.config_path:
            path = Path(self.config_path)
            return path if path.exists() else None

        # Search in current directory and parents
        current = Path.cwd()
        for _ in range(5):  # Search up to 5 levels
            for config_name in CONFIG_FILE_NAMES:
                config_file = current / config_name
                if config_file.exists():
                    return config_file
            parent = current.parent
            if parent == current:  # Reached root
                break
            current = parent

        return None

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            import yaml
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            raise ImportError(
                "PyYAML is required for YAML config files. "
                "Install with: pip install pyyaml"
            )
        except Exception as e:
            raise ValueError(f"Failed to load YAML config from {path}: {e}")

    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load JSON config from {path}: {e}")

    def load_from_file(self) -> 'ConfigLoader':
        """
        Load configuration from file if available.

        Returns:
            Self for method chaining
        """
        config_file = self._find_config_file()
        if not config_file:
            return self

        # Load based on file extension
        if config_file.suffix in ['.yaml', '.yml']:
            file_config = self._load_yaml(config_file)
        elif config_file.suffix == '.json':
            file_config = self._load_json(config_file)
        else:
            raise ValueError(f"Unsupported config file format: {config_file.suffix}")

        # Merge file config (overrides defaults)
        self._config.update(file_config)
        return self

    def load_from_env(self) -> 'ConfigLoader':
        """
        Load configuration from environment variables.

        Environment variables should be prefixed with CLI_TOOL_
        Example: CLI_TOOL_TIMEOUT=60

        Returns:
            Self for method chaining
        """
        env_mapping = {
            'CLI_TOOL_TIMEOUT': 'timeout',
            'CLI_TOOL_ENABLE_CACHE': 'enable_cache',
            'CLI_TOOL_CACHE_SIZE': 'cache_size',
            'CLI_TOOL_MAX_FILE_SIZE': 'max_file_size',
            'CLI_TOOL_LOG_LEVEL': 'log_level',
        }

        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Type conversion
                if config_key in ['timeout', 'cache_size', 'max_file_size']:
                    self._config[config_key] = int(value)
                elif config_key == 'enable_cache':
                    self._config[config_key] = value.lower() in ['true', '1', 'yes']
                else:
                    self._config[config_key] = value

        return self

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()


def load_config(config_path: Optional[str] = None) -> ConfigLoader:
    """
    Load configuration from all sources.

    Args:
        config_path: Optional explicit path to config file

    Returns:
        ConfigLoader instance with merged configuration
    """
    loader = ConfigLoader(config_path)
    loader.load_from_file().load_from_env()
    return loader
