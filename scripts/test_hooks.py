#!/usr/bin/env python3
"""Hook tests. Run: python3 scripts/test_hooks.py

Invokes the hooks as subprocesses so the real stdin/stdout contract is covered,
not just the matching helper.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
EDIT = "after-composer-edit.py"
STOP = "stop-verify.py"

# (script, payload, should_fire)
CASES: list[tuple[str, dict, bool]] = [
    (EDIT, {"file_path": "/app/src/screens.ts"}, True),
    (EDIT, {"file_path": "/app/src/registry.ts"}, True),
    (EDIT, {"file_path": "/app/src/screens/home.tsx"}, True),
    (EDIT, {"file_path": "/a/composers/cart.ts"}, True),
    (EDIT, {"file_path": "/app/src/screens.test.ts"}, True),
    (EDIT, {"uri": "file:///app/src/Registry.TS"}, True),
    (EDIT, {"path": "C:\\app\\src\\screens.ts"}, True),
    (EDIT, {"edits": [{"a": {"file_path": "/x/screens.ts"}}]}, True),
    # Prose must never fire; only real path-valued keys count.
    (EDIT, {"message": "let's refactor the composer layer"}, False),
    (EDIT, {"message": "look at screens.ts sometime"}, False),
    (EDIT, {"file_path": "/layout-service/README.md"}, False),
    (EDIT, {"file_path": "/layout-service/src/ports.ts"}, False),
    (EDIT, {"file_path": "/app/src/button.css"}, False),
    (EDIT, {"file_path": "/app/screenshots/a.ts"}, False),
    (EDIT, {}, False),
    # Hexagon rings, Java only.
    (EDIT, {"file_path": "/api/src/main/java/com/acme/catalog/domain/Product.java"}, True),
    (EDIT, {"file_path": "/api/src/main/java/com/acme/catalog/application/ListProductsService.java"}, True),
    (EDIT, {"file_path": "/api/src/main/java/com/acme/catalog/application/port/out/Products.java"}, True),
    (EDIT, {"file_path": "/api/src/main/java/com/acme/catalog/adapter/in/web/ProductController.java"}, True),
    (EDIT, {"file_path": "/api/src/main/java/com/acme/catalog/adapter/out/legacy/ProductsAdapter.java"}, True),
    (EDIT, {"file_path": "/api/src/main/java/com/acme/hexagon/UseCase.java"}, True),
    (EDIT, {"file_path": "/api/src/main/java/com/acme/legacy/CatalogService.java"}, False),
    (EDIT, {"file_path": "/api/src/main/resources/application.yml"}, False),
    (EDIT, {"file_path": "/app/src/domain/order.ts"}, False),
    (STOP, {"edits": [{"path": "/app/src/screens.ts"}]}, True),
    (STOP, {"edits": [{"path": "/api/src/main/java/com/acme/catalog/domain/Order.java"}]}, True),
    (STOP, {"summary": "discussed the composer design"}, False),
    (STOP, {"edits": [{"path": "/app/a.css"}]}, False),
]

MALFORMED = [(EDIT, "not json"), (STOP, ""), (EDIT, "[1,2,3]"), (STOP, "null")]


def run(script: str, raw: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        input=raw,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    failures: list[str] = []

    for script, payload, should_fire in CASES:
        code, out, err = run(script, json.dumps(payload))
        fired = out != "{}"
        if fired != should_fire or code != 0 or err:
            failures.append(f"{script} {payload} -> fired={fired} exit={code} {err}")

    # Every failure mode must emit {} and exit 0, never block the user.
    for script, raw in MALFORMED:
        code, out, err = run(script, raw)
        if out != "{}" or code != 0:
            failures.append(f"{script} <- {raw!r} -> {out!r} exit={code}")

    code, out, _ = run(STOP, json.dumps({"edits": [{"path": "/app/src/screens.ts"}] * 2}))
    if out.count("/app/src/screens.ts") != 1:
        failures.append(f"stop hook did not dedupe paths: {out}")

    code, out, _ = run(
        STOP, json.dumps({"edits": [{"path": f"/app/screens/p{i}.ts"} for i in range(5)]})
    )
    if "+2 more" not in out:
        failures.append(f"stop hook did not truncate long path lists: {out}")

    both = json.dumps(
        {
            "edits": [
                {"path": "/app/src/screens.ts"},
                {"path": "/api/src/main/java/com/acme/catalog/domain/Order.java"},
            ]
        }
    )
    for script, first, second in ((EDIT, "validateScreen", "ArchUnit"), (STOP, "Composer files", "Hexagon files")):
        _, out, _ = run(script, both)
        if first not in out or second not in out:
            failures.append(f"{script} did not report both kinds of edit: {out}")

    for line in failures:
        print(f"FAIL {line}")
    total = len(CASES) + len(MALFORMED) + 4
    print(f"{total - len(failures)}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
