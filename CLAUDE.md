# AGENT.md

This file provides guidance to AI agents when working with code in this repository.

## Development Commands

This project uses `uv` for package management:

```bash
# Install dependencies
uv sync

# Run tests (NOTE: No tests currently exist - pytest not configured)
uv run pytest

# Run single test (when tests exist)
uv run pytest tests/test_specific.py::test_function_name -v

# Run the server locally for testing (single backend mode)
uv run omni-fs-mcp-stdio "memory:///"
uv run omni-fs-mcp-http "memory:///"

# Run with multi-backend configuration
uv run omni-fs-mcp-stdio examples/demo_config.json
uv run omni-fs-mcp-http --config examples/demo_config.json --port 8080

# Build package (optimized with hatchling)
uv build

# Install development version
uv add -e .

# Validate build configuration
uv build --check

# Code quality (NOTE: No linting/formatting tools configured yet)
# Consider adding: ruff check src/ (for linting)
# Consider adding: ruff format src/ (for formatting)
# Consider adding: mypy src/ (for type checking)
```

## Architecture Overview

Omni-FS-MCP is an MCP (Model Context Protocol) server that provides unified access to multiple file systems simultaneously through OpenDAL. The architecture consists of three main layers:

### Core Components

1. **mcp_server.py** - Multi-backend MCP server implementation using FastMCP
   - Defines 13 MCP tools: 7 file operations + 6 backend management tools
   - File operations: list_files, read_file, write_file, copy_file, rename_file, create_dir, stat_file
   - Backend management: register_backend, list_backends, set_default_backend, remove_backend, check_backend_health, get_backend_stats
   - Handles dual transport modes: stdio (local) and streamable-http (remote)
   - Supports both single backend (backward compatible) and multi-backend modes
   - Entry points: `main()`, `run_stdio()`, `run_http()`

2. **backend_manager.py** - Central management of multiple DAL instances
   - `BackendManager` class manages multiple named backends
   - `BackendConfig` class for structured backend configuration
   - Health monitoring and connection validation
   - Read-only backend support with write operation protection
   - Default backend handling for seamless operations

3. **dal.py** - Data Access Layer wrapping OpenDAL
   - `DAL` class provides abstraction over OpenDAL operators
   - URL parsing to extract schema and connection options
   - Lazy initialization of OpenDAL operator instances
   - Comprehensive logging for all operations

### Multi-Backend Architecture

The server supports multiple file system backends simultaneously:
- **Named Backends**: Each backend has a unique identifier (e.g., "local", "s3-prod", "backup")
- **Default Backend**: One backend is designated as default for operations without explicit backend specification
- **Cross-Backend Operations**: Files can be copied between different backends
- **Backend Types**: Local filesystem, S3, WebDAV, FTP, HTTP, in-memory, and others via OpenDAL

### Configuration Management

- **JSON Configuration**: Backends can be defined in JSON configuration files
- **Runtime Registration**: Backends can be added/removed during server operation
- **Validation**: Connection validation during backend registration
- **Security**: Read-only backend protection prevents accidental modifications

### Transport Modes

The server supports two distinct transport mechanisms:
- **stdio**: For local integrations and CLI tools
- **streamable-http**: For remote connections and web applications

### Backward Compatibility

The server maintains full backward compatibility with single-backend configurations:
- Single URL argument creates a default backend
- Existing MCP tools work without modification
- Legacy command-line interfaces continue to function

## Testing

Use the memory backend for development and testing:

```bash
# Single backend mode
uv run omni-fs-mcp-stdio "memory:///"

# Multi-backend mode with configuration
uv run omni-fs-mcp-stdio examples/demo_config.json
```

All file operations are logged with comprehensive error handling and debug information.

## Common Development Tasks

### Adding New Backend Types
1. Ensure OpenDAL supports the backend type
2. Add URL scheme documentation to README.md
3. Add example configuration to README.md
4. Test connection validation and operations

### Testing Multi-Backend Features
```bash
# Create test configuration with multiple backends
echo '{
  "backends": [
    {"name": "memory1", "url": "memory:///", "default": true},
    {"name": "memory2", "url": "memory:///"}
  ]
}' > test_config.json

# Test with configuration
uv run omni-fs-mcp-stdio test_config.json
```

### Debugging Backend Issues
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Provides detailed logs of backend operations, connections, and errors
```

## Build System

The project uses **hatchling** as the build backend (2024-2025 best practice):
- Modern PEP 517/621 compliant build system
- Maintained by PyPA (Python Packaging Authority)
- Superior to legacy setuptools for new projects
- Explicit package discovery with `src` layout
- Optimized wheel and sdist generation