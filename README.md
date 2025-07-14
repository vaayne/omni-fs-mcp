# Omni-FS MCP Server

Omni-FS-MCP is an MCP (Model Context Protocol) server that supports managing multiple types of file systems, such as local FS, S3, R2, B2, WebDAV, and others, in one MCP server. It is built on top of OpenDAL.

## Features

- **Multiple File System Support**: Works with local filesystem, S3, R2, B2, WebDAV, and other OpenDAL-supported backends
- **Dual Transport Support**: Supports both stdio and streamable-http transports
- **Comprehensive File Operations**: List, read, write, copy, rename, create directories, and get file statistics
- **Modern Python Packaging**: Uses uv for fast dependency management

## Installation

```bash
# Install using uv (recommended)
uv add omni-fs-mcp

# Or install using pip
pip install omni-fs-mcp
```

## Usage

### Command Line Interface

The server supports multiple ways to run depending on your transport needs:

#### 1. General Command (supports both transports)
```bash
# Stdio transport (default)
omni-fs-mcp <url> --transport stdio

# HTTP transport
omni-fs-mcp <url> --transport streamable-http
```

#### 2. Transport-Specific Commands

**For stdio transport (local connections):**
```bash
omni-fs-mcp-stdio <url>
```

**For HTTP transport (remote connections):**
```bash
omni-fs-mcp-http <url>
```

### URL Examples

The URL parameter specifies which file system backend to use:

```bash
# Local filesystem
omni-fs-mcp-stdio "fs:///"

# S3
omni-fs-mcp-http "s3://bucket-name?region=us-east-1&access_key_id=xxx&secret_access_key=yyy"

# WebDAV
omni-fs-mcp-stdio "webdav://example.com/webdav?username=user&password=pass"

# Memory (for testing)
omni-fs-mcp-stdio "memory:///"
```

### Transport Modes

#### Stdio Transport
- **Use case**: Local integrations, development, CLI tools
- **Advantages**: Simple setup, no network configuration
- **Communication**: Standard input/output streams
- **Example**: `omni-fs-mcp-stdio "fs:///"`

#### Streamable HTTP Transport
- **Use case**: Remote connections, web applications, cloud deployments
- **Advantages**: Network accessible, scalable, cloud-friendly
- **Communication**: HTTP with bidirectional streaming
- **Example**: `omni-fs-mcp-http "s3://my-bucket" --port 8080`

## Available Tools

The MCP server provides the following tools:

1. **list_files(path="/")** - List files and directories
2. **read_file(path)** - Read file contents as text
3. **write_file(path, content)** - Write content to a file
4. **copy_file(src, dst)** - Copy files or directories
5. **rename_file(src, dst)** - Rename or move files/directories
6. **create_dir(path)** - Create a directory
7. **stat_file(path)** - Get file/directory metadata

## Development

```bash
# Clone the repository
git clone <repository-url>
cd omni-fs-mcp

# Install development dependencies
uv sync

# Run tests
uv run pytest

# Run the server in development
uv run omni-fs-mcp-stdio "memory:///"
```

## Supported File Systems

Thanks to OpenDAL, this MCP server supports numerous storage backends:

- **Local**: Local filesystem (`fs://`)
- **Cloud Storage**: S3, R2, B2, GCS, Azure Blob
- **Network**: WebDAV, FTP, SFTP
- **In-Memory**: Memory storage for testing
- **And many more**: See [OpenDAL documentation](https://opendal.apache.org/) for the full list

## License

This project is licensed under the MIT License.
