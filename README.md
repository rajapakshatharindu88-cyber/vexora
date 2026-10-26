# VEXORA [by Grafio.]

Creator: R.M.T.D Rajapaksha · Owner: Grafio. · Target version 1.0.0 · Date 2026/10/26

VEXORA is a vector-design and print-production desktop app. It is a derivative of
[VectorCraft](https://github.com/storytold/vectorcraft) 0.17.0 (Rust, egui; MIT OR Apache-2.0).

## Honest status

This repository is a **baseline**: the unmodified VectorCraft 0.17.0 code, with VEXORA's logo
as the app icon and a GitHub Actions workflow that builds a Linux x86_64 AppImage and ZIP.

| Item | State |
|---|---|
| CI workflow that builds, tests, packages | Written. **Not yet run**: this file will not say it works until a run has succeeded. |
| AppImage | Produced only by a successful workflow run. None is checked into this repo. |
| VEXORA icon (resized from the supplied logo) | Done in assets; visible only on dark backgrounds (the logo is near-white). |
| Window title, About dialog (creator, owner, date, version, Grafio. logo) | **Not done**: still VectorCraft text; needs Rust changes. |
| ArtCraft Discord/website links in the app | **Still present** in code; to be replaced. |
| Die-line, fold-line, QR, calendar, barcode, AI image panel, preflight | **Not implemented.** |

Everything not marked done is not done. The next stage starts only after the baseline run is green.

## Build it

See [`docs/vexora/BEGINNER_GUIDE.md`](docs/vexora/BEGINNER_GUIDE.md) (step by step) and [`BUILDING.md`](BUILDING.md).

## Licences and logos

Original VectorCraft notices are preserved in `LICENSE-MIT`, `LICENSE-APACHE` and `NOTICE`.
The ArtCraft logos were removed (trademarks, not licensed for forks). The VEXORA and Grafio. logos in
`branding/` belong to Grafio.; their licence terms are for the owner to state. The upstream README is
kept as `upstream/README.vectorcraft.md`.
