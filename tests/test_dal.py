"""Tests for the DAL (Data Access Layer) module."""


from omni_fs_mcp.dal import DAL


class TestDAL:
    """Test cases for DAL class."""

    def test_init_with_options(self):
        """Test DAL initialization with options."""
        schema = "memory"
        options = {"key": "value"}
        dal = DAL(schema, options)

        assert dal.schema == schema
        assert dal.options == options

    def test_init_without_options(self):
        """Test DAL initialization without options."""
        schema = "memory"
        dal = DAL(schema)

        assert dal.schema == schema
        assert dal.options == {}

    def test_from_url_memory(self):
        """Test creating DAL from memory URL."""
        url = "memory:///"
        dal = DAL.from_url(url)

        assert dal.schema == "memory"
        assert isinstance(dal.options, dict)

    def test_from_url_with_query_params(self):
        """Test creating DAL from URL with query parameters."""
        url = "memory:///?param1=value1&param2=value2"
        dal = DAL.from_url(url)

        assert dal.schema == "memory"
        assert dal.options["param1"] == "value1"
        assert dal.options["param2"] == "value2"

    def test_from_url_fs(self):
        """Test creating DAL from filesystem URL."""
        url = "fs:///"
        dal = DAL.from_url(url)

        assert dal.schema == "fs"
        assert isinstance(dal.options, dict)
