# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is a **content repository** for the GeoDev Slovenia meetup community — not a software project. It stores per-event materials (READMEs, slides, demo code, photos, banner art) plus a top-level README that announces upcoming meetups and tracks the roadmap. There is no build, test, or lint pipeline; changes are reviewed for content correctness.

Most prose (READMEs, talk abstracts) is written in **Slovenian**. Match the language of the surrounding file when editing — do not translate existing Slovenian content to English unless asked.

## Layout conventions

- Each event lives in a folder named `YYYY-NN-meetup/` where `NN` is the **sequential meetup number** (not the month). E.g. `2025-14-meetup/` is meetup #14 held in 2025. Workshops use `YYYY-NN-workshop/`. Preserve this pattern when adding new events.
- Inside an event folder, each talk goes in a numbered subdirectory: `01-<slug>`, `02-<slug>`, ... containing the speaker's slides (PDF) and any demo code/data. A `photos/` subdirectory holds event photos.
- Event-level `README.md` follows a fixed template — see `2025-14-meetup/README.md` or `2025-13-meetup/README.md` as the current reference. Required sections, in order:
  - Title `# GeoDev Meetup #N`
  - 📍 Lokacija, 📅 Datum, 🕕 Čas (emoji + bold label)
  - `## Program` with one block per talk: bold title, time range, abstract, speaker name + affiliation, `---` separator between talks
  - `## Ostalo` (free-form: registration link, sponsor thanks, etc.)
- Branding assets (raccoon logo, banners) live in `resources/`. Per-event promotional images (banners, social cards, A3 print) live at the root of that event's folder.

## When announcing a new meetup

Update **both** files:
1. The new event's `YYYY-NN-meetup/README.md` (from the template above).
2. The top-level `README.md` "Next Meetups" section — change the headline event, update the roadmap checklist (✅ done / 🎯 planned), and link to the new event folder.

## Rendering banners

Per-event folders can contain HTML banner files (e.g. `banner-story.html`, `banner-landscape.html`) that embed inline SVG and Google Fonts. To export them as PNG, use `scripts/banner-to-png.js` — a Playwright-based screenshotter that screenshots the `.banner` element at a configurable device-pixel ratio.

One-time setup:

```
cd scripts && npm install && npx playwright install chromium
```

Run from `scripts/`:

```
node banner-to-png.js ../2026-15-meetup/banner-*.html          # 2× DPR (default)
node banner-to-png.js ../2026-15-meetup/banner-story.html --scale=1   # native pixels
```

PNGs land next to each source HTML by default (override with `--out=DIR`). The script expects the HTML to have a `.banner` element with explicit CSS width/height. `node_modules/` and `package-lock.json` under `scripts/` are gitignored.

## Submodules

`2017-02-meetup/02_R_Shiny_application/geodev-meetup-app` is a git submodule pointing at <https://github.com/zkuralt/geodev-meetup-app>. Don't edit files inside it from this repo.
