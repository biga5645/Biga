"""Conversation memory — stores and manages the message history sent to the LLM."""

from typing import List, Dict, Any


class ConversationMemory:
    """Maintains the full message history for a single agent session."""

    def __init__(self, system_prompt: str):
        self._messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})

    def add_assistant(self, message: Dict[str, Any]) -> None:
        """Append a raw assistant message dict (may include tool_calls)."""
        self._messages.append(message)

    def add_tool_result(self, tool_call_id: str, content: str) -> None:
        self._messages.append(
            {"role": "tool", "tool_call_id": tool_call_id, "content": content}
        )

    # ------------------------------------------------------------------
    # Read-only access
    # ------------------------------------------------------------------

    @property
    def messages(self) -> List[Dict[str, Any]]:
        return list(self._messages)

    def __len__(self) -> int:
        return len(self._messages)
