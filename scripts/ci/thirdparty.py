#!/usr/bin/env python3
"""Turn `cargo metadata --format-version 1 --locked` (stdin) into THIRD_PARTY_CRATES.md (stdout)."""
import json, sys
m = json.load(sys.stdin)
ws = set(m.get("workspace_members", []))
rows = []
for p in m["packages"]:
    if p["id"] in ws:
        continue
    src = p.get("source") or "path"
    src = "crates.io" if src.startswith("registry+") else ("git: " + src.split("#")[0][4:] if src.startswith("git+") else src)
    rows.append((p["name"], p["version"], p.get("license") or p.get("license_file") or "UNKNOWN (check upstream)", src))
rows.sort(key=lambda r: (r[0].lower(), r[1]))
print("# Third-party Rust crates in this build\n")
print("Generated from the locked dependency graph (`cargo metadata --locked`). The license column is the")
print("SPDX expression the crate declares; it is not legal advice. Non-crate assets are in NOTICE and ASSETS.md.\n")
print(f"Total: {len(rows)} crates\n")
print("| Crate | Version | Declared license | Source |\n|---|---|---|---|")
for r in rows:
    print("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
unk = [r for r in rows if r[2].startswith("UNKNOWN")]
if unk:
    print(f"\n**{len(unk)} crate(s) declare no license metadata** and need manual review.")
