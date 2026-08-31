"""Shared path matching for the SDUI hooks.

Both hooks answer two questions: did this payload touch a file that *composes a
screen tree*, or one *inside a hexagon*? Matching is deliberately narrow. A nag
that fires on unrelated work gets ignored, which is worse than no nag at all.
"""

from __future__ import annotations

import posixpath
from collections.abc import Callable

# Only keys whose values are genuinely file paths. Walking arbitrary strings
# makes any prose mentioning a composer look like a file edit.
PATH_KEYS = {"file_path", "filePath", "path", "uri", "file"}

CODE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}

# A composer lives in a file named for it, or in a directory of them.
COMPOSER_STEMS = {"screens", "registry", "composer", "composers"}
COMPOSER_DIRS = {"screens", "composers"}

# Hexagon source lives in a package named for the ring it belongs to. Java-only,
# so a `domain/` folder of TypeScript models in the frontend does not fire.
HEXAGON_DIRS = {"domain", "application", "adapter", "hexagon"}


def _normalize(value: str) -> str:
    if value.startswith("file://"):
        value = value[len("file://") :]
    return value.replace("\\", "/").lower()


def _is_composer_path(value: str) -> bool:
    path = _normalize(value)
    base = posixpath.basename(path)
    stem, dot, suffix = base.rpartition(".")
    if not dot or f".{suffix}" not in CODE_SUFFIXES:
        return False

    # screens.ts, registry.ts, screens.test.ts -> leading segment is the stem.
    if stem.split(".")[0] in COMPOSER_STEMS:
        return True

    return any(part in COMPOSER_DIRS for part in posixpath.dirname(path).split("/"))


def _is_hexagon_path(value: str) -> bool:
    path = _normalize(value)
    if not path.endswith(".java"):
        return False

    return any(part in HEXAGON_DIRS for part in posixpath.dirname(path).split("/"))


def collect_path_values(payload: object) -> list[str]:
    found: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in PATH_KEYS and isinstance(value, str):
                    found.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)
    return found


def _touched(payload: object, matches: Callable[[str], bool]) -> list[str]:
    seen: dict[str, None] = {}
    for value in collect_path_values(payload):
        if matches(value):
            seen.setdefault(value, None)
    return list(seen)


def touched_composers(payload: object) -> list[str]:
    """Composer-ish paths in the payload, deduped and in first-seen order."""
    return _touched(payload, _is_composer_path)


def touched_hexagon(payload: object) -> list[str]:
    """Hexagon Java paths in the payload, deduped and in first-seen order."""
    return _touched(payload, _is_hexagon_path)
