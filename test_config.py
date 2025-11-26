"""
Unit tests for the config module.
"""

import unittest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
from config import ConfigLoader, load_config, VERSION, APP_NAME


class TestConfigLoader(unittest.TestCase):
    """Test cases for ConfigLoader class."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='test_config_')
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_default_configuration(self):
        """Test that default values are loaded correctly."""
        loader = ConfigLoader()
        self.assertEqual(loader.get('version'), VERSION)
        self.assertEqual(loader.get('app_name'), APP_NAME)
        self.assertEqual(loader.get('timeout'), 30)
        self.assertTrue(loader.get('enable_cache'))
        self.assertEqual(loader.get('cache_size'), 128)

    def test_get_with_default(self):
        """Test get() method with default value."""
        loader = ConfigLoader()
        self.assertEqual(loader.get('nonexistent_key', 'default'), 'default')
        self.assertIsNone(loader.get('nonexistent_key'))

    def test_to_dict(self):
        """Test to_dict() returns a copy of configuration."""
        loader = ConfigLoader()
        config_dict = loader.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertIn('version', config_dict)

        # Verify it's a copy, not the original
        config_dict['version'] = 'modified'
        self.assertNotEqual(loader.get('version'), 'modified')

    def test_load_json_config(self):
        """Test loading configuration from JSON file."""
        config_data = {
            'timeout': 60,
            'enable_cache': False,
            'log_level': 'DEBUG'
        }
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump(config_data, f)

        loader = ConfigLoader()
        loader.load_from_file()

        self.assertEqual(loader.get('timeout'), 60)
        self.assertFalse(loader.get('enable_cache'))
        self.assertEqual(loader.get('log_level'), 'DEBUG')

    def test_load_yaml_config(self):
        """Test loading configuration from YAML file."""
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")

        config_file = Path(self.temp_dir) / '.cli-tool.yaml'
        with open(config_file, 'w') as f:
            f.write("""
timeout: 120
enable_cache: false
cache_size: 256
log_level: WARNING
""")

        loader = ConfigLoader()
        loader.load_from_file()

        self.assertEqual(loader.get('timeout'), 120)
        self.assertFalse(loader.get('enable_cache'))
        self.assertEqual(loader.get('cache_size'), 256)
        self.assertEqual(loader.get('log_level'), 'WARNING')

    def test_yaml_import_error_handling(self):
        """Test that missing PyYAML produces helpful error message."""
        config_file = Path(self.temp_dir) / '.cli-tool.yaml'
        with open(config_file, 'w') as f:
            f.write("timeout: 60")

        loader = ConfigLoader()

        # Simulate ImportError when trying to import yaml module
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == 'yaml':
                raise ImportError("No module named 'yaml'")
            return real_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=mock_import):
            with self.assertRaises(ImportError) as cm:
                loader.load_from_file()
            self.assertIn('PyYAML is required', str(cm.exception))
            self.assertIn('pip install pyyaml', str(cm.exception).lower())

    def test_explicit_config_path(self):
        """Test loading config from explicit path."""
        custom_config = Path(self.temp_dir) / 'custom-config.json'
        with open(custom_config, 'w') as f:
            json.dump({'timeout': 99}, f)

        loader = ConfigLoader(config_path=str(custom_config))
        loader.load_from_file()

        self.assertEqual(loader.get('timeout'), 99)

    def test_config_file_not_found(self):
        """Test that missing config file doesn't raise error."""
        loader = ConfigLoader(config_path='/nonexistent/path.json')
        loader.load_from_file()  # Should not raise
        # Should fall back to defaults
        self.assertEqual(loader.get('timeout'), 30)

    def test_malformed_json_config(self):
        """Test error handling for malformed JSON."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            f.write('{invalid json}')

        loader = ConfigLoader()
        with self.assertRaises(ValueError) as cm:
            loader.load_from_file()
        self.assertIn('Failed to load JSON config', str(cm.exception))

    def test_parent_directory_search(self):
        """Test that config files are found in parent directories."""
        # Create config in parent directory
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': 77}, f)

        # Create subdirectory and change to it
        subdir = Path(self.temp_dir) / 'subdir1' / 'subdir2'
        subdir.mkdir(parents=True)
        os.chdir(subdir)

        loader = ConfigLoader()
        loader.load_from_file()

        # Should find config from parent directory
        self.assertEqual(loader.get('timeout'), 77)

    def test_load_from_env(self):
        """Test loading configuration from environment variables."""
        env_vars = {
            'CLI_TOOL_TIMEOUT': '90',
            'CLI_TOOL_ENABLE_CACHE': 'false',
            'CLI_TOOL_CACHE_SIZE': '512',
            'CLI_TOOL_LOG_LEVEL': 'ERROR'
        }

        with patch.dict(os.environ, env_vars):
            loader = ConfigLoader()
            loader.load_from_env()

            self.assertEqual(loader.get('timeout'), 90)
            self.assertFalse(loader.get('enable_cache'))
            self.assertEqual(loader.get('cache_size'), 512)
            self.assertEqual(loader.get('log_level'), 'ERROR')

    def test_env_bool_conversion(self):
        """Test boolean conversion from environment variables."""
        test_cases = {
            'true': True,
            'True': True,
            'TRUE': True,
            '1': True,
            'yes': True,
            'false': False,
            'False': False,
            'FALSE': False,
            '0': False,
            'no': False,
        }

        for value, expected in test_cases.items():
            with patch.dict(os.environ, {'CLI_TOOL_ENABLE_CACHE': value}):
                loader = ConfigLoader()
                loader.load_from_env()
                self.assertEqual(loader.get('enable_cache'), expected,
                               f"Failed for value: {value}")

    def test_method_chaining(self):
        """Test that load methods support method chaining."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': 50}, f)

        with patch.dict(os.environ, {'CLI_TOOL_CACHE_SIZE': '256'}):
            loader = ConfigLoader()
            result = loader.load_from_file().load_from_env()

            # Verify method chaining returns self
            self.assertIs(result, loader)

            # Verify both sources were loaded
            self.assertEqual(loader.get('timeout'), 50)  # From file
            self.assertEqual(loader.get('cache_size'), 256)  # From env

    def test_config_priority(self):
        """Test that configuration sources have correct priority."""
        # File config
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': 40}, f)

        # Env var should override file
        with patch.dict(os.environ, {'CLI_TOOL_TIMEOUT': '80'}):
            loader = ConfigLoader()
            loader.load_from_file()
            loader.load_from_env()

            # Env var should win (loaded last)
            self.assertEqual(loader.get('timeout'), 80)

    def test_load_config_helper_function(self):
        """Test the load_config() convenience function."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': 100}, f)

        with patch.dict(os.environ, {'CLI_TOOL_CACHE_SIZE': '1024'}):
            config = load_config()

            self.assertIsInstance(config, ConfigLoader)
            self.assertEqual(config.get('timeout'), 100)
            self.assertEqual(config.get('cache_size'), 1024)

    def test_validation_string_to_int_conversion(self):
        """Test that string values are converted to integers when needed."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': '50'}, f)

        loader = ConfigLoader()
        loader.load_from_file()

        # Should convert string "50" to int 50
        self.assertEqual(loader.get('timeout'), 50)
        self.assertIsInstance(loader.get('timeout'), int)

    def test_validation_invalid_integer(self):
        """Test that invalid integer values raise helpful errors."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': 'not a number'}, f)

        loader = ConfigLoader()
        with self.assertRaises(ValueError) as cm:
            loader.load_from_file()

        error_msg = str(cm.exception)
        self.assertIn('timeout', error_msg)
        self.assertIn('not a number', error_msg)

    def test_validation_negative_value(self):
        """Test that negative values for numeric fields are rejected."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'timeout': -10}, f)

        loader = ConfigLoader()
        with self.assertRaises(ValueError) as cm:
            loader.load_from_file()

        self.assertIn('must be positive', str(cm.exception))

    def test_validation_invalid_log_level(self):
        """Test that invalid log levels are rejected with helpful message."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'log_level': 'INVALID'}, f)

        loader = ConfigLoader()
        with self.assertRaises(ValueError) as cm:
            loader.load_from_file()

        error_msg = str(cm.exception)
        self.assertIn('log_level', error_msg)
        self.assertIn('INVALID', error_msg)
        self.assertIn('DEBUG', error_msg)  # Should list valid options

    def test_validation_log_level_case_normalization(self):
        """Test that log levels are normalized to uppercase."""
        config_file = Path(self.temp_dir) / '.cli-tool.json'
        with open(config_file, 'w') as f:
            json.dump({'log_level': 'debug'}, f)

        loader = ConfigLoader()
        loader.load_from_file()

        # Should normalize to uppercase
        self.assertEqual(loader.get('log_level'), 'DEBUG')


if __name__ == '__main__':
    unittest.main()
