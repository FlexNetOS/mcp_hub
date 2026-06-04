#!/usr/bin/env python3
"""Validate the mcp_hub catalog.

Checks registry.json entries against the schema rules, that referenced doc/snippet
files exist and parse, that ids are unique and well-formed, and that the README catalog
table links each server. Dependency-free (stdlib only). Exits non-zero on any problem.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KIND = {"local", "external", "remote"}
RUNNER = {"binary", "npx", "docker", "http"}
TRANSPORT = {"stdio", "http", "sse"}
STATUS = {"stable", "beta", "experimental", "deprecated"}
AUTH = {"none", "oauth", "api-key"}
REQUIRED = ["id", "displayName", "kind", "runner", "transport", "status", "auth",
            "summary", "doc", "snippet"]
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

errors = []


def err(msg):
    errors.append(msg)


def main():
    reg_path = ROOT / "registry.json"
    try:
        reg = json.loads(reg_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"FATAL: cannot read registry.json: {e}")
        return 1

    for key in ("version", "updated", "org", "servers"):
        if key not in reg:
            err(f"registry.json missing top-level key: {key}")

    servers = reg.get("servers", [])
    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    seen_ids = set()

    for i, s in enumerate(servers):
        sid = s.get("id", f"<index {i}>")
        for field in REQUIRED:
            if field not in s:
                err(f"[{sid}] missing required field: {field}")

        if "id" in s:
            if not ID_RE.match(s["id"]):
                err(f"[{sid}] id is not kebab-case: {s['id']!r}")
            if s["id"] in seen_ids:
                err(f"[{sid}] duplicate id")
            seen_ids.add(s["id"])

        for field, allowed in (("kind", KIND), ("runner", RUNNER),
                               ("transport", TRANSPORT), ("status", STATUS),
                               ("auth", AUTH)):
            if field in s and s[field] not in allowed:
                err(f"[{sid}] {field}={s[field]!r} not in {sorted(allowed)}")

        # conditional rules
        if s.get("transport") == "stdio" and not s.get("command"):
            err(f"[{sid}] stdio transport requires 'command'")
        if s.get("kind") == "remote" and not s.get("url"):
            err(f"[{sid}] remote kind requires 'url'")

        # referenced files exist
        for ref in ("doc", "snippet"):
            if ref in s:
                p = ROOT / s[ref]
                if not p.exists():
                    err(f"[{sid}] {ref} file not found: {s[ref]}")
                elif ref == "snippet":
                    try:
                        json.loads(p.read_text())
                    except json.JSONDecodeError as e:
                        err(f"[{sid}] snippet is not valid JSON: {e}")

        # README links the server's snippet + doc
        if readme:
            for ref in ("snippet", "doc"):
                if ref in s and s[ref] not in readme:
                    err(f"[{sid}] README.md does not link {ref}: {s[ref]}")

    if errors:
        print(f"✗ {len(errors)} problem(s) in the catalog:\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"✓ catalog OK — {len(servers)} servers, all entries valid and consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
