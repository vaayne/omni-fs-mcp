# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `uv` for package management:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run the server locally for testing
uv run omni-fs-mcp-stdio "memory:///"
uv run omni-fs-mcp-http "memory:///"

# Build package (optimized with hatchling)
uv build

# Install development version
uv add -e .

# Validate build configuration
uv build --check
```

## Architecture Overview

Omni-FS-MCP is an MCP (Model Context Protocol) server that provides unified access to multiple file systems through OpenDAL. The architecture consists of three main layers:

### Core Components

1. **mcp_server.py** - Main MCP server implementation using FastMCP
   - Defines 7 MCP tools: list_files, read_file, write_file, copy_file, rename_file, create_dir, stat_file
   - Handles dual transport modes: stdio (local) and streamable-http (remote)
   - Entry points: `main()`, `run_stdio()`, `run_http()`

2. **dal.py** - Data Access Layer wrapping OpenDAL
   - `DAL` class provides abstraction over OpenDAL operators
   - URL parsing to extract schema and connection options
   - Lazy initialization of OpenDAL operator instances
   - Comprehensive logging for all operations

3. **URL-based Backend Selection** - File system backends are selected via URL schemes:
   - `fs:///` - Local filesystem
   - `s3://bucket?region=...&access_key_id=...` - AWS S3
   - `webdav://host/path?username=...&password=...` - WebDAV
   - `memory:///` - In-memory storage (testing)

### Transport Modes

The server supports two distinct transport mechanisms:
- **stdio**: For local integrations and CLI tools
- **streamable-http**: For remote connections and web applications

### Global State Management

The server uses a global DAL client instance (`_client`) that must be initialized with a URL before any operations. This singleton pattern ensures consistent connection handling across all MCP tool calls.

## Testing

Use the memory backend for development and testing:
```bash
uv run omni-fs-mcp-stdio "memory:///"
```

All file operations are logged with comprehensive error handling and debug information.

## Build System

The project uses **hatchling** as the build backend (2024-2025 best practice):
- Modern PEP 517/621 compliant build system
- Maintained by PyPA (Python Packaging Authority)
- Superior to legacy setuptools for new projects
- Explicit package discovery with `src` layout
- Optimized wheel and sdist generation