# Biga AI Agent 🤖

A ready-to-use, tool-calling AI agent built with Python and the OpenAI API.

## Features

- 💬 **Conversational** — maintains full session memory
- 🔧 **Tool calling** — the agent can use tools autonomously:
  - `calculate` — safe math expression evaluator
  - `web_search` — web search (stub; plug in SerpAPI / Tavily)
  - `read_file` / `write_file` — local filesystem access
- 🔌 **Extensible** — add new tools in minutes (see [Adding Tools](#adding-tools))

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

### 3. Run the agent

```bash
python main.py
```

## Project Structure

```
Biga/
├── main.py              # CLI entry point
├── requirements.txt
├── .env.example
├── agent/
│   ├── agent.py         # Core agent loop (tool-calling)
│   └── memory.py        # Conversation history
└── tools/
    ├── __init__.py      # Tool registry
    ├── calculator.py    # Math evaluator
    ├── web_search.py    # Web search (stub)
    └── file_ops.py      # read_file / write_file
```

## Adding Tools

1. Create a new file in `tools/`, e.g. `tools/my_tool.py`.
2. Define a `MY_TOOL_SCHEMA` dict (OpenAI function schema) and a `my_tool(**kwargs)` function.
3. Register them in `tools/__init__.py` by adding to `TOOL_DEFINITIONS` and `TOOL_HANDLERS`.

## Enabling Web Search

Set `SEARCH_API_KEY` in your `.env` and uncomment the provider code in `tools/web_search.py`.
[Tavily](https://tavily.com/) is recommended (`pip install tavily-python`).

## Requirements

- Python 3.9+
- OpenAI API key (GPT-4o or GPT-3.5-turbo)
