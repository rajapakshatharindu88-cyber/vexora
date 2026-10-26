#!/usr/bin/env bash
# VEXORA: icons come from branding/vexora-logo.png (resize only), not from the upstream dragon SVG.
set -euo pipefail
exec python3 "$(dirname "${BASH_SOURCE[0]}")/vexora_icons.py"
