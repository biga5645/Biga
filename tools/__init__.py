"""Tool registry — maps tool names to handler functions and their JSON schemas."""

from tools.calculator import calculate, CALCULATE_SCHEMA
from tools.web_search import web_search, WEB_SEARCH_SCHEMA
from tools.file_ops import read_file, write_file, READ_FILE_SCHEMA, WRITE_FILE_SCHEMA

# List of OpenAI tool definitions (passed to the API)
TOOL_DEFINITIONS = [
    {"type": "function", "function": CALCULATE_SCHEMA},
    {"type": "function", "function": WEB_SEARCH_SCHEMA},
    {"type": "function", "function": READ_FILE_SCHEMA},
    {"type": "function", "function": WRITE_FILE_SCHEMA},
]

# Dispatch table: tool name -> callable
TOOL_HANDLERS = {
    "calculate": calculate,
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
}
