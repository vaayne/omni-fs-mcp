"""Tests for the MCP Server module."""

import json
import tempfile
import pytest
from omni_fs_mcp.mcp_server import load_config_from_file, backend_manager


class TestMCPServer:
    """Test cases for MCP Server functions."""

    def test_load_config_from_file_valid(self):
        """Test loading valid configuration from file."""
        config_data = {
            "backends": [
                {
                    "name": "test1",
                    "url": "memory:///",
                    "description": "Test backend 1",
                    "default": True
                },
                {
                    "name": "test2",
                    "url": "memory:///",
                    "description": "Test backend 2"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        # Clear any existing backends
        backend_manager.backends.clear()
        backend_manager.configs.clear()
        backend_manager.default_backend = None
        
        # Load configuration
        load_config_from_file(config_file)
        
        # Verify backends were loaded
        assert "test1" in backend_manager.backends
        assert "test2" in backend_manager.backends
        assert backend_manager.default_backend is not None

    def test_load_config_from_file_not_found(self):
        """Test loading configuration from non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_config_from_file("nonexistent_config.json")

    def test_load_config_from_file_invalid_json(self):
        """Test loading configuration from invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            config_file = f.name
        
        with pytest.raises(json.JSONDecodeError):
            load_config_from_file(config_file)

    def test_load_config_empty_backends(self):
        """Test loading configuration with empty backends list."""
        config_data = {"backends": []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        # This should not raise an error
        load_config_from_file(config_file)
