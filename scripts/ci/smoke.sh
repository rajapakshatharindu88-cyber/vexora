#!/usr/bin/env bash
# Startup checks of the built AppImage. Usage: smoke.sh <AppImage> <out-dir> [repo-root]
# These checks prove only what they say (see report). They do NOT test drawing, saving or exporting.
set -uo pipefail
APPIMAGE="$(realpath "$1")"; OUT="$(realpath -m "$2")"; ROOT="$(realpath "${3:-.}")"
mkdir -p "$OUT"; chmod +x "$APPIMAGE"; RES="$OUT/smoke-results.txt"; : >"$RES"
rec() { echo "$1" | tee -a "$RES"; }

WORK="$(mktemp -d)"; cd "$WORK" || exit 1
if "$APPIMAGE" --appimage-extract >"$OUT/smoke-extract.log" 2>&1 && [[ -d squashfs-root ]]; then
  rec "extract: ok"
else
  rec "extract: FAILED (see smoke-extract.log)"; exit 1
fi
if squashfs-root/usr/bin/vectorcraft-cli --version >"$OUT/smoke-cli.log" 2>&1; then
  rec "cli_version: ok ($(head -n1 "$OUT/smoke-cli.log"))"; CLI=0
else
  rec "cli_version: FAILED (see smoke-cli.log)"; CLI=1
fi
rec "desktop_name: $(grep -m1 '^Name=' squashfs-root/*.desktop || echo MISSING)"
if cmp -s squashfs-root/.DirIcon "$ROOT/assets/app-icon/hicolor/256x256/apps/ai.storyteller.vectorcraft.png"; then
  rec "appimage_icon_matches_repo_256: yes"
else
  rec "appimage_icon_matches_repo_256: NO"; CLI=1
fi
# Startup under a virtual display for 25 s. Exit code 124 = still running when the timer killed it.
APPIMAGE_EXTRACT_AND_RUN=1 LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s "-screen 0 1280x800x24" \
  timeout 25 "$APPIMAGE" >"$OUT/smoke-gui.log" 2>&1
GUI=$?
if [[ $GUI -eq 124 ]]; then
  rec "gui_startup: still running after 25 s under Xvfb (started without crashing; NOT a functional test)"; GUIOK=0
else
  rec "gui_startup: FAILED, exited with code $GUI before 25 s (see smoke-gui.log)"; GUIOK=1
fi
[[ $CLI -eq 0 && $GUIOK -eq 0 ]]
