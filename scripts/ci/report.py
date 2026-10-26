#!/usr/bin/env python3
"""Write BUILD_REPORT.md from what actually happened. Usage: report.py <ci-out-dir>
Inputs (env): OUT_FETCH OUT_BUILD OUT_TESTS OUT_PACKAGE OUT_SMOKE (success|failure|skipped|cancelled|''),
RUN_TESTS (true/false), RUNNER, GITHUB_SHA. Nothing is claimed that its step outcome does not support."""
import os, re, pathlib, hashlib, sys, platform, datetime
ci = pathlib.Path(sys.argv[1]); logs = ci / "logs"; dist = ci / "dist"
E = lambda k: (os.environ.get(k) or "not run").lower()
steps = [("Fetch locked dependencies", "OUT_FETCH"), ("Release build", "OUT_BUILD"),
         ("Baseline tests", "OUT_TESTS"), ("AppImage + tar packaging", "OUT_PACKAGE"),
         ("AppImage startup checks", "OUT_SMOKE")]
sym = {"success": "PASSED", "failure": "FAILED", "skipped": "SKIPPED", "cancelled": "CANCELLED"}

def tests():
    f = logs / "03-test.log"
    if not f.is_file(): return None
    t = f.read_text(errors="replace")
    tot = dict(passed=0, failed=0, ignored=0, suites=0)
    for m in re.finditer(r"test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored", t):
        tot["passed"] += int(m[1]); tot["failed"] += int(m[2]); tot["ignored"] += int(m[3]); tot["suites"] += 1
    tot["failed_names"] = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", t, re.M)))[:50]
    tot["compile_error"] = bool(re.search(r"^error(\[E\d+\])?:", t, re.M)) and tot["suites"] == 0
    return tot

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

L = ["# VEXORA baseline build report", "",
     f"- Generated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
     f"- Source commit: `{os.environ.get('GITHUB_SHA', 'unknown')}`",
     f"- Runner image: `{os.environ.get('RUNNER', 'unknown')}` ({platform.platform()})",
     "- Base: VectorCraft 0.17.0 source snapshot (NOT 0.13.1). In-app text still says VectorCraft: see Limitations.", "",
     "## Step results (from the actual workflow run)", "", "| Step | Result |", "|---|---|"]
for name, key in steps:
    L.append(f"| {name} | {sym.get(E(key), E(key).upper())} |")
tr = tests()
L += ["", "## Test detail", ""]
if os.environ.get("RUN_TESTS") == "false":
    L.append("Tests were not run: they were switched off for this run.")
elif E("OUT_TESTS") in ("skipped", "not run") and tr is None:
    L.append("Tests did not run because an earlier stage (fetch or build) did not succeed.")
elif tr is None:
    L.append("No test log exists: the tests did not start.")
else:
    L.append(f"`cargo test --release --locked --no-fail-fast`: {tr['passed']} passed, {tr['failed']} failed, "
             f"{tr['ignored']} ignored, across {tr['suites']} test suites.")
    if tr["compile_error"]: L.append("\nThe test build had a compile error, so no test results were produced. See logs/03-test.log.")
    if tr["failed_names"]: L += ["", "Failing tests (first 50):", ""] + [f"- `{n}`" for n in tr["failed_names"]]
L += ["", "## What the AppImage checks do and do not show", ""]
sm = ci / "logs" / "smoke-results.txt"
L.append(sm.read_text() and "```\n" + sm.read_text().strip() + "\n```" if sm.is_file() else "Startup checks did not run.")
L += ["", "Startup checks show only: the AppImage extracts, the bundled CLI prints a version, the packaged icon is the VEXORA icon,",
      "and the GUI stayed alive for 25 s under a virtual display. They do **not** test drawing, saving, opening, exporting,",
      "keyboard/mouse use or high-DPI. Those need manual QA on a real desktop.", "", "## Output files", "",
      "| File | Size (bytes) | SHA-256 |", "|---|---|---|"]
files = sorted(p for p in dist.glob("*") if p.is_file() and p.suffix not in (".zsync",)) if dist.is_dir() else []
for p in files: L.append(f"| `{p.name}` | {p.stat().st_size} | `{sha(p)}` |")
if not files: L.append("| (none produced) | | |")
L += ["", "## Limitations of this baseline (not yet done)", "",
      "- The window title, About dialog, ArtCraft/Discord links and all in-app strings are still VectorCraft/ArtCraft (Rust code is unchanged).",
      "- Not implemented: die-line and fold-line tools, QR/calendar/barcode generators, AI image panel, print preflight. No claim is made about them.",
      "- Built on one Linux image only; compatibility with other distributions is untested (needs glibc at least as new as the runner's).",
      "- The VEXORA logo is near-white on transparent: it is nearly invisible on light launchers/backgrounds."]
(ci / "BUILD_REPORT.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
