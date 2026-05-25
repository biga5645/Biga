"""File read/write tools for the agent."""

import os

READ_FILE_SCHEMA = {
    "name": "read_file",
    "description": "Read the contents of a local file and return them as a string.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Absolute or relative path to the file to read.",
            }
        },
        "required": ["path"],
    },
}

WRITE_FILE_SCHEMA = {
    "name": "write_file",
    "description": "Write (or overwrite) content to a local file.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Absolute or relative path to the file to write.",
            },
            "content": {
                "type": "string",
                "description": "The text content to write to the file.",
            },
        },
        "required": ["path", "content"],
    },
}

_MAX_READ_BYTES = 100_000  # 100 KB safety cap


def read_file(path: str) -> str:
    """Read a file and return its contents."""
    try:
        size = os.path.getsize(path)
        if size > _MAX_READ_BYTES:
            return f"Error: file is too large ({size} bytes). Maximum is {_MAX_READ_BYTES} bytes."
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as exc:
        return f"Error reading file: {exc}"


def write_file(path: str, content: str) -> str:
    """Write content to a file, creating parent directories if needed."""
    try:
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return f"Successfully wrote {len(content)} characters to {path}."
    except Exception as exc:
        return f"Error writing file: {exc}"
