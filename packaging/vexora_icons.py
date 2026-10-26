#!/usr/bin/env python3
"""Generate VEXORA's icon files from branding/vexora-logo.png.

RESIZE ONLY: the supplied logo is never redrawn, recoloured, cropped, padded or given a
background. Resizing is done on premultiplied alpha so transparent edges get no dark fringe.
Output file names keep the historical "vectorcraft" names because Rust code (include_bytes!)
and packaging scripts refer to those exact paths.

Needs: python3, Pillow, numpy.   Usage: python3 packaging/vexora_icons.py
"""
import base64, io, pathlib, sys
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "branding" / "vexora-logo.png"
OUT = ROOT / "assets" / "app-icon"
APP_ID = "ai.storyteller.vectorcraft"  # unchanged on purpose: window class, icon theme name, file paths


def resize(im: Image.Image, size: int) -> Image.Image:
    a = np.asarray(im.convert("RGBA"), dtype=np.float32) / 255.0
    al = a[..., 3:4]
    pre = np.concatenate([a[..., :3] * al, al], axis=2)
    ch = [np.asarray(Image.fromarray(pre[..., i], mode="F").resize((size, size), Image.LANCZOS)) for i in range(4)]
    o = np.clip(np.stack(ch, axis=2), 0.0, 1.0)
    al2 = o[..., 3:4]
    rgb = np.where(al2 > 1e-6, o[..., :3] / np.maximum(al2, 1e-6), 0.0)
    out = np.concatenate([np.clip(rgb, 0, 1), al2], axis=2)
    return Image.fromarray((out * 255.0 + 0.5).astype(np.uint8), mode="RGBA")


def png_bytes(im: Image.Image) -> bytes:
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()


def svg_wrapper(png: bytes, size: int) -> str:
    # The raster logo embedded as-is (no tracing/redrawing), so the SVG looks exactly like the PNG.
    b64 = base64.b64encode(png).decode()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<image width="{size}" height="{size}" xlink:href="data:image/png;base64,{b64}"/></svg>\n')


def main() -> int:
    if not SRC.is_file():
        print(f"missing {SRC}", file=sys.stderr); return 1
    src = Image.open(SRC).convert("RGBA")
    if src.width != src.height:
        print("logo is not square; refusing to pad or crop it", file=sys.stderr); return 1
    for s in (16, 24, 32, 48, 64, 128, 256, 512):
        d = OUT / "hicolor" / f"{s}x{s}" / "apps"; d.mkdir(parents=True, exist_ok=True)
        (d / f"{APP_ID}.png").write_bytes(png_bytes(resize(src, s)))
    (OUT / "vectorcraft-1024.png").write_bytes(png_bytes(resize(src, 1024)))
    (OUT / "vectorcraft-macos-512.png").write_bytes(png_bytes(resize(src, 512)))  # plain resize, no Apple margin
    svg = svg_wrapper(png_bytes(resize(src, 512)), 512)
    for p in (OUT / "vectorcraft.svg", OUT / "vectorcraft-small.svg", OUT / "hicolor" / "scalable" / "apps" / f"{APP_ID}.svg"):
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(svg)
    sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
    resize(src, 256).save(OUT / "vectorcraft.ico", format="ICO", sizes=[(s, s) for s in sizes])
    resize(src, 1024).save(OUT / "vectorcraft.icns", format="ICNS")
    print("icons written to", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
