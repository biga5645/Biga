"""Core agent loop — handles the OpenAI tool-calling cycle."""

import json
import os
from typing import Optional

from openai import OpenAI

from agent.memory import ConversationMemory
from tools import TOOL_DEFINITIONS, TOOL_HANDLERS

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, concise AI assistant. "
    "Use the available tools whenever they help you answer accurately. "
    "Think step-by-step when solving complex problems."
)


class Agent:
    """A tool-calling agent backed by the OpenAI Chat Completions API."""

    def __init__(
        self,
        model: Optional[str] = None,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        api_key: Optional[str] = None,
    ):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.memory = ConversationMemory(system_prompt)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def chat(self, user_message: str) -> str:
        """Send a user message, run the tool loop, and return the final reply."""
        self.memory.add_user(user_message)
        return self._run_loop()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_loop(self) -> str:
        """Agentic loop: call model → handle tool calls → repeat until done."""
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.memory.messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            choice = response.choices[0]
            message = choice.message

            # Store the assistant turn (may include tool_calls)
            self.memory.add_assistant(message.model_dump(exclude_unset=True, exclude_none=True))

            # If no tool calls, we have our final answer
            if not message.tool_calls:
                return message.content or ""

            # Execute each requested tool
            for tool_call in message.tool_calls:
                result = self._dispatch_tool(tool_call)
                self.memory.add_tool_result(tool_call.id, result)

    def _dispatch_tool(self, tool_call) -> str:
        """Look up and execute the requested tool; return the string result."""
        name = tool_call.function.name
        try:
            args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as exc:
            return f"Error: could not parse tool arguments: {exc}"

        handler = TOOL_HANDLERS.get(name)
        if handler is None:
            return f"Error: unknown tool '{name}'"

        try:
            return str(handler(**args))
        except Exception as exc:
            return f"Error executing tool '{name}': {exc}"
