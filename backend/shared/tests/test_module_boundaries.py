"""
Modular-monolith rule: a module may use another module only through its
public services, selectors or events, never its models, api or tasks.
Test files are exempt: they may build fixtures from any module.
"""

import ast
from pathlib import Path

MODULES_DIR = Path(__file__).resolve().parents[2] / "modules"
PUBLIC_PARTS = {"services", "selectors", "events"}


def _imported_names(path: Path):
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            yield node.module, [alias.name for alias in node.names]
        elif isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name, []


def test_modules_only_use_each_others_public_api():
    violations = []
    for path in MODULES_DIR.rglob("*.py"):
        if "tests" in path.parts:
            continue
        owner = path.relative_to(MODULES_DIR).parts[0]
        for module, names in _imported_names(path):
            parts = module.split(".")
            if parts[0] != "modules" or len(parts) < 2 or parts[1] == owner:
                continue
            # "from modules.identity import selectors" or "modules.identity.selectors"
            used = {parts[2]} if len(parts) > 2 else set(names)
            if not used <= PUBLIC_PARTS:
                violations.append(f"{path.relative_to(MODULES_DIR)} imports {module} {names}")
    assert violations == []
