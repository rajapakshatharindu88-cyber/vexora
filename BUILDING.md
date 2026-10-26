# Building VEXORA (baseline)

## Recommended: GitHub Actions (no local setup)
Follow `docs/vexora/BEGINNER_GUIDE.md`. The workflow is `.github/workflows/vexora-build.yml`.

## Locally (Linux x86_64, Ubuntu 24.04 tested only by the CI recipe, not by hand)
```bash
sudo apt-get install -y pkg-config libxkbcommon-dev libwayland-dev libx11-dev libxcb1-dev libxcursor-dev \
  libxrandr-dev libxi-dev libfontconfig1-dev libfreetype-dev libgl1-mesa-dev mesa-vulkan-drivers xvfb zip curl desktop-file-utils
rustup toolchain install 1.97.0 --profile minimal && rustup default 1.97.0   # workspace needs >= 1.95
cargo fetch --locked
cargo build --release --locked -p vectorcraft -p vectorcraft-cli
xvfb-run -a cargo test --release --locked --no-fail-fast
bash packaging/linux/package.sh --skip-build --formats "appimage tar"   # output in dist/release/
```
`package.sh` downloads appimagetool and the AppImage runtime from GitHub and checks pinned SHA-256 sums.
Needs network access to crates.io, github.com. Official upstream builds also embed extra fonts via
`CRAFT_FONTS_DIR`; this baseline does not, so some CJK/Arabic text may fall back to other fonts.

## Regenerate icons
`python3 packaging/vexora_icons.py` (needs Pillow, numpy). Resize only.
