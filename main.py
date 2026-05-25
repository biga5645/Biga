#!/usr/bin/env python3
"""Entry point — interactive CLI for the Biga AI Agent."""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from agent.agent import Agent  # noqa: E402 (import after dotenv)

BANNER = """
╔══════════════════════════════════════╗
║         🤖  Biga AI Agent            ║
║  Type your message, or 'exit' / 'q'  ║
║  to quit.  Type 'reset' to start a   ║
║  fresh conversation.                 ║
╚══════════════════════════════════════╝
"""


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "Error: OPENAI_API_KEY is not set.\n"
            "Copy .env.example to .env and add your key."
        )
        sys.exit(1)

    print(BANNER)

    agent = Agent()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            agent = Agent()
            print("Conversation reset.\n")
            continue

        try:
            reply = agent.chat(user_input)
            print(f"\nAgent: {reply}\n")
        except Exception as exc:
            print(f"\n[Error] {exc}\n")


if __name__ == "__main__":
    main()
