#!/usr/bin/env python3
"""Fail-open: remind validateScreen on composer edits, ArchUnit on hexagon edits."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _sdui_paths import touched_composers, touched_hexagon  # noqa: E402

COMPOSER_REMINDER = (
    "Composed SDUI trees must pass validateScreen against the host component "
    "registry. Use the sdui-verify skill; do not ship unknown types or extra props."
)

HEXAGON_REMINDER = (
    "Hexagon code must keep domain and application free of Spring, JPA, servlet, "
    "and Hibernate types, and the endpoint contract unchanged. Use the scute-hexagon "
    "skill; the ArchUnit gate stays scoped to the converted base package."
)


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        print("{}")
        return

    reminders = []
    if touched_composers(payload):
        reminders.append(COMPOSER_REMINDER)
    if touched_hexagon(payload):
        reminders.append(HEXAGON_REMINDER)

    if reminders:
        print(json.dumps({"additional_context": " ".join(reminders)}))
        return

    print("{}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("{}")
