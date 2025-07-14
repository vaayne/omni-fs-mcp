import logging
from typing import Any, Dict, List

import opendal
from mcp.server.fastmcp import FastMCP

from omni_fs_mcp.dal import DAL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Omni-FS MCP Server")
logger.info("Initialized FastMCP server: Omni-FS MCP Server")

# Global DAL instance (will be initialized when first used)
_client = None


def get_client() -> DAL:
    """Get or create DAL client instance."""
    global _client
    if _client is None:
        logger.error("Attempted to get DAL client before initialization")
        raise ValueError("DAL client not initialized")
    return _client


def init_client(url: str):
    """Initialize the global DAL client with the provided URL."""
    global _client
    logger.info(f"Initializing DAL client with URL: {url}")
    _client = DAL.from_url(url)
    logger.info("DAL client initialized successfully")


@mcp.tool()
def list_files(path: str = "/") -> List[Dict[str, Any]]:
    """
    List files and directories in the specified path.

    Args:
        path: The directory path to list, always ending with a slash ("/").

    Returns:
        List of entries with their metadata
    """
    logger.info(f"Listing files in path: {path}")
    client = get_client()
    entries = []

    # Iterate through all entries in the specified path
    for entry in client.list(path):
        entries.append(
            {
                "path": entry.path,
            }
        )

    logger.info(f"Found {len(entries)} entries in path: {path}")
    return entries


@mcp.tool()
def read_file(path: str) -> str:
    """
    Read the contents of a file from the file system.

    Args:
        path: The file path to read

    Returns:
        The file contents as a string
    """
    logger.info(f"Reading file: {path}")
    client = get_client()

    # Read the file data as bytes
    data = client.read(path)

    # Decode bytes to UTF-8 string
    content = data.decode("utf-8")
    logger.info(f"Successfully read file: {path} ({len(content)} characters)")
    return content


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Write content to a file on the file system.

    Args:
        path: The file path to write to
        content: The content to write

    Returns:
        Success message
    """
    logger.info(f"Writing file: {path} ({len(content)} characters)")
    client = get_client()

    # Encode string content to bytes before writing
    client.write(path, content.encode("utf-8"))
    logger.info(f"Successfully wrote file: {path}")
    return f"Successfully wrote to {path}"


@mcp.tool()
def copy_file(src: str, dst: str) -> str:
    """
    Copy a file or directory on the file system.

    Args:
        src: Source path
        dst: Destination path

    Returns:
        Success message
    """
    logger.info(f"Copying file from {src} to {dst}")
    client = get_client()

    # Perform the copy operation
    client.copy(src, dst)
    logger.info(f"Successfully copied {src} to {dst}")
    return f"Successfully copied {src} to {dst}"


@mcp.tool()
def rename_file(src: str, dst: str) -> str:
    """
    Rename or move a file or directory on the file system.

    Args:
        src: Source path
        dst: Destination path

    Returns:
        Success message
    """
    logger.info(f"Renaming/moving file from {src} to {dst}")
    client = get_client()

    # Perform the rename/move operation
    client.rename(src, dst)
    logger.info(f"Successfully renamed {src} to {dst}")
    return f"Successfully renamed {src} to {dst}"


@mcp.tool()
def create_dir(path: str) -> str:
    """
    Create a directory on the file system.

    Args:
        path: The directory path to create

    Returns:
        Success message
    """
    logger.info(f"Creating directory: {path}")
    client = get_client()

    # Create the directory
    client.create_dir(path)
    logger.info(f"Successfully created directory: {path}")
    return f"Successfully created directory {path}"


@mcp.tool()
def stat_file(path: str) -> opendal.Metadata:
    """
    Get metadata/statistics for a file or directory on the file system.

    Args:
        path: The path to get stats for

    Returns:
        File metadata
    """
    logger.info(f"Getting metadata for: {path}")
    client = get_client()

    # Retrieve metadata for the specified path
    metadata = client.stat(path)
    logger.info(f"Successfully retrieved metadata for: {path}")

    return metadata


def main():
    """Main entry point for the MCP server."""
    import argparse

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Omni-FS MCP Server")
    parser.add_argument("url", help="URL to initialize DAL client")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mechanism to use (default: stdio)",
    )
    # parser.add_argument(
    #     "--port",
    #     type=int,
    #     default=8000,
    #     help="Port to listen on for streamable-http transport (default: 8000)",
    # )
    # parser.add_argument(
    #     "--host",
    #     default="localhost",
    #     help="Host to bind to for streamable-http transport (default: localhost)",
    # )
    args = parser.parse_args()

    logger.info(f"Starting Omni-FS MCP Server with URL: {args.url}")
    logger.info(f"Using transport: {args.transport}")

    # Initialize the DAL client with the provided URL
    init_client(args.url)

    # Start the MCP server with the specified transport
    if args.transport == "stdio":
        logger.info("Starting MCP server with stdio transport")
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        # logger.info(
        #     f"Starting MCP server with streamable-http transport on {args.host}:{args.port}"
        # )
        mcp.run(transport="streamable-http")


def run_stdio():
    """Run the MCP server with stdio transport for local connections."""
    import sys

    if len(sys.argv) < 2:
        logger.error("URL argument required")
        print("Usage: omni-fs-mcp-stdio <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    logger.info("Starting Omni-FS MCP Server with stdio transport")
    logger.info(f"Initializing with URL: {url}")
    init_client(url)
    mcp.run(transport="stdio")


def run_http():
    """Run the MCP server with streamable-http transport for remote connections."""
    import argparse

    parser = argparse.ArgumentParser(description="Omni-FS MCP Server (HTTP)")
    parser.add_argument("url", help="URL to initialize DAL client")
    # parser.add_argument(
    #     "--host", default="localhost", help="Host to bind to (default: localhost)"
    # )
    # parser.add_argument(
    #     "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    # )
    args = parser.parse_args()

    logger.info("Starting Omni-FS MCP Server with streamable-http transport")
    # logger.info(f"Server will listen on {args.host}:{args.port}")
    logger.info(f"Initializing with URL: {args.url}")
    init_client(args.url)
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
