#!/usr/bin/env python3
"""Fail-open stop hook: nudge sdui-verify when composers or hexagon code changed."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _sdui_paths import touched_composers, touched_hexagon  # noqa: E402


def listing(paths: list[str]) -> str:
    listed = ", ".join(paths[:3])
    if len(paths) > 3:
        listed += f", +{len(paths) - 3} more"
    return listed


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        print("{}")
        return

    composers = touched_composers(payload)
    hexagon = touched_hexagon(payload)
    if not composers and not hexagon:
        print("{}")
        return

    messages = []
    if composers:
        messages.append(
            f"Composer files changed ({listing(composers)}). Follow sdui-verify: "
            "contract-test these trees against the host registry before finishing."
        )
    if hexagon:
        messages.append(
            f"Hexagon files changed ({listing(hexagon)}). Follow sdui-verify: run the "
            "ArchUnit gate and use-case tests, and confirm the endpoint contract is "
            "unchanged before finishing."
        )

    print(json.dumps({"followup_message": " ".join(messages)}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("{}")
