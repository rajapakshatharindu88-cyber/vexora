#!/usr/bin/env bash
# Guard: the supplied logos must be unchanged, and no ArtCraft logo may ship.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
( cd branding && sha256sum -c SHA256SUMS )
if [[ -e docs/brand ]] || find . -path ./target -prune -o -iname 'artcraft-*' -print | grep -q .; then
  echo "error: ArtCraft logo files are present; they are trademarks and must not be shipped" >&2; exit 1
fi
for s in 16 24 32 48 64 128 256 512; do
  f="assets/app-icon/hicolor/${s}x${s}/apps/ai.storyteller.vectorcraft.png"
  [[ -s "$f" ]] || { echo "error: missing $f" >&2; exit 1; }
done
echo "branding check OK: logos unchanged, no ArtCraft logos, icon set present"
