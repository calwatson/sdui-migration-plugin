#!/usr/bin/env python3
"""Fail-open: remind validateScreen when a screen composer is edited."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _sdui_paths import touched_composers  # noqa: E402

REMINDER = (
    "Composed SDUI trees must pass validateScreen against the host component "
    "registry. Use the sdui-verify skill; do not ship unknown types or extra props."
)


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        print("{}")
        return

    if touched_composers(payload):
        print(json.dumps({"additional_context": REMINDER}))
        return

    print("{}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("{}")
