"""Tests for the Backend Manager module."""

import pytest
from omni_fs_mcp.backend_manager import BackendManager, BackendConfig


class TestBackendConfig:
    """Test cases for BackendConfig class."""

    def test_valid_config(self):
        """Test creating a valid backend configuration."""
        config = BackendConfig(
            name="test",
            url="memory:///",
            description="Test backend",
            readonly=False
        )
        
        assert config.name == "test"
        assert config.url == "memory:///"
        assert config.description == "Test backend"
        assert config.readonly is False

    def test_invalid_name_empty(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Backend name must be a non-empty string"):
            BackendConfig(name="", url="memory:///")

    def test_invalid_name_special_chars(self):
        """Test that invalid characters in name raise ValueError."""
        with pytest.raises(ValueError, match="Backend name can only contain"):
            BackendConfig(name="test@backend", url="memory:///")

    def test_invalid_url_empty(self):
        """Test that empty URL raises ValueError."""
        with pytest.raises(ValueError, match="Backend URL must be a non-empty string"):
            BackendConfig(name="test", url="")

    def test_invalid_url_format(self):
        """Test that invalid URL format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid URL format"):
            BackendConfig(name="test", url="not-a-url")


class TestBackendManager:
    """Test cases for BackendManager class."""

    def test_init(self):
        """Test BackendManager initialization."""
        manager = BackendManager()
        
        assert isinstance(manager.backends, dict)
        assert isinstance(manager.configs, dict)
        assert manager.default_backend is None
        assert len(manager.backends) == 0

    def test_register_backend_memory(self):
        """Test registering a memory backend."""
        manager = BackendManager()
        
        result = manager.register_backend(
            name="test",
            url="memory:///",
            description="Test memory backend",
            validate_connection=False  # Skip connection validation for tests
        )
        
        assert result is True
        assert "test" in manager.backends
        assert "test" in manager.configs
        assert manager.default_backend == "test"

    def test_get_backend_default(self):
        """Test getting the default backend."""
        manager = BackendManager()
        manager.register_backend(
            name="test",
            url="memory:///",
            validate_connection=False
        )
        
        backend = manager.get_backend()
        assert backend is not None

    def test_get_backend_by_name(self):
        """Test getting backend by name."""
        manager = BackendManager()
        manager.register_backend(
            name="test",
            url="memory:///",
            validate_connection=False
        )
        
        backend = manager.get_backend("test")
        assert backend is not None

    def test_get_backend_not_found(self):
        """Test that getting non-existent backend raises ValueError."""
        manager = BackendManager()
        
        with pytest.raises(ValueError, match="Backend 'nonexistent' not found"):
            manager.get_backend("nonexistent")

    def test_list_backends_empty(self):
        """Test listing backends when none are registered."""
        manager = BackendManager()
        backends = manager.list_backends()
        
        assert isinstance(backends, list)
        assert len(backends) == 0

    def test_list_backends_with_data(self):
        """Test listing backends with registered backends."""
        manager = BackendManager()
        manager.register_backend(
            name="test",
            url="memory:///",
            description="Test backend",
            validate_connection=False
        )
        
        backends = manager.list_backends()
        assert len(backends) == 1
        assert backends[0]["name"] == "test"
        assert backends[0]["url"] == "memory:///"
        assert backends[0]["is_default"] is True

    def test_set_default_backend(self):
        """Test setting default backend."""
        manager = BackendManager()
        manager.register_backend(name="test1", url="memory:///", validate_connection=False)
        manager.register_backend(name="test2", url="memory:///", validate_connection=False)
        
        manager.set_default_backend("test2")
        assert manager.default_backend == "test2"

    def test_remove_backend(self):
        """Test removing a backend."""
        manager = BackendManager()
        manager.register_backend(name="test1", url="memory:///", validate_connection=False)
        manager.register_backend(name="test2", url="memory:///", validate_connection=False)
        
        # Set test2 as default, then remove test1
        manager.set_default_backend("test2")
        manager.remove_backend("test1")
        assert "test1" not in manager.backends
        assert "test2" in manager.backends

    def test_get_backend_stats(self):
        """Test getting backend statistics."""
        manager = BackendManager()
        manager.register_backend(
            name="test",
            url="memory:///",
            readonly=True,
            validate_connection=False
        )
        
        stats = manager.get_backend_stats()
        assert stats["total_backends"] == 1
        assert stats["default_backend"] == "test"
        assert stats["readonly_backends"] == 1
        assert "memory" in stats["backend_schemes"]
