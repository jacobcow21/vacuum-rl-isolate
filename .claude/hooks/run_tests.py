#!/usr/bin/env python3
"""PostToolUse hook: run the test suite after any Python file in src/ or
tests/ changes. On failure, the test output is sent back to Claude (exit
code 2) so it fixes the problem before moving on.
"""

import json
import os
import subprocess
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = data.get("tool_input", {}).get("file_path", "").replace("\\", "/")
    if not path.endswith(".py") or not ("/src/" in path or "/tests/" in path):
        return 0

    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        tail = "\n".join(result.stdout.strip().splitlines()[-25:])
        print(f"Tests failed after editing {path}:\n{tail}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
