#!/usr/bin/env python3
"""PreToolUse hook: keep the hidden model (T and R) out of the agent.

Q-learning is model-free, so src/agent.py must not use the environment's
WALLS, TERMINAL_REWARDS or START constants. If an edit to src/agent.py
would add any of them, the edit is blocked (exit code 2) and the reason is
sent back to Claude.
"""

import json
import re
import sys

FORBIDDEN = ("WALLS", "TERMINAL_REWARDS", "START")


def new_text(tool_input: dict) -> str:
    parts = [tool_input.get("content", ""), tool_input.get("new_string", "")]
    for edit in tool_input.get("edits", []) or []:
        parts.append(edit.get("new_string", ""))
    return "\n".join(p for p in parts if p)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_input = data.get("tool_input", {})
    path = tool_input.get("file_path", "")
    if not path.replace("\\", "/").endswith("src/agent.py"):
        return 0

    text = new_text(tool_input)
    found = [name for name in FORBIDDEN if re.search(rf"\b{name}\b", text)]
    if found:
        print(
            f"Blocked: src/agent.py may not use {', '.join(found)}. "
            "The agent is model-free and must learn only from env.step() "
            "results (T and R are unknown).",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
