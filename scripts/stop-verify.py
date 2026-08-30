#!/usr/bin/env python3
"""Fail-open stop hook: nudge sdui-verify when composers were edited this session."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _sdui_paths import touched_composers  # noqa: E402


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        print("{}")
        return

    touched = touched_composers(payload)
    if not touched:
        print("{}")
        return

    listed = ", ".join(touched[:3])
    if len(touched) > 3:
        listed += f", +{len(touched) - 3} more"

    print(
        json.dumps(
            {
                "followup_message": (
                    f"Composer files changed ({listed}). Follow sdui-verify: "
                    "contract-test these trees against the host registry before "
                    "finishing."
                )
            }
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("{}")
