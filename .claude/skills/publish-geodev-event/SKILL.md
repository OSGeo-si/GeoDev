---
name: publish-geodev-event
description: End-to-end publish a new GeoDev Slovenija meetup — creates the event folder in this repo, the landing-page entry, the three HTML banners (story / landscape / square) + their PNGs, and the promo copy file (LinkedIn, newsletter, Luma, Discord, Twitter/X, short blurb). Use when the user wants to add/announce/publish a new GeoDev meetup — phrases like "add GeoDev #N", "publish next meetup", "make the new event", "set up GeoDev <number>".
---

# Publish a new GeoDev Slovenija meetup

End-to-end checklist that mirrors the workflow in the top-level `README.md` → "Publishing a New Event 📣" section. **Don't deviate** from the file layout or template — past meetups depend on it.

## Inputs the user must provide

Before doing anything, confirm with `AskUserQuestion` (in one batched call) anything missing:

1. **Meetup number** `N` (next sequential — check the roadmap in the top-level `README.md`).
2. **Date** (full date, day of week).
3. **Time** (default `18:00`).
4. **Location** (default UIRS, Trnovski pristan 2 — the recurring venue).
5. **Speakers** — for each: full name + title/affiliation, talk title, **and** a paragraph-sized abstract from them.
6. **Luma URL** — they'll create the Luma event after the banners exist (since the square banner is the cover). If they don't have it yet, leave `{{LUMA_URL}}` placeholders and tell them which files to update once they do.

If the user already pointed at source material (e.g. a draft `geodev-N.md` in the landing-page repo at `/Users/nejcdougan/OSGeoSi/landing-page/content/events/geodev/`), pull from there first.

## Folder naming

Event folder is `YYYY-N-meetup/` at the repo root — **year = event year, N = sequential meetup number (not month)**. Examples: `2025-14-meetup`, `2026-15-meetup`. Workshops use `YYYY-N-workshop/`.

## Step 1 — Create the event folder + README

```
mkdir -p YYYY-N-meetup
```

Copy `2026-15-meetup/README.md` as the template. Sections in order:

1. `# GeoDev Meetup #N`
2. 📍 `__Lokacija:__ ...` (link UIRS to <https://www.uirs.si/sl-si/>, link "Vhod iz pasaže" to <https://www.openstreetmap.org/node/12504450770>)
3. 📅 `__Datum:__ ...`
4. 🕕 `__Čas:__ ...`
5. `## Program` — for each talk: `__Title__\n<time-range>\n<abstract>\n\n<speaker>` separated by `---`. Use `__bold__` (double underscore), not `**`. Match the format of `2025-14-meetup/README.md` exactly.
6. `## Ostalo` — closing line, **registration link line**, and host credit.

Slovenian prose. Match the language of surrounding meetups — do not translate to English.

## Step 2 — Update top-level README.md

* Change the "Next Meetups 🚀" headline date / link to the new folder.
* Mark previous event ✅ on the roadmap, add a new row 🎯 for the new event.

## Step 3 — Add the landing-page entry

Repo: `/Users/nejcdougan/OSGeoSi/landing-page/`. Create `content/events/geodev/geodev-N.md` with frontmatter (mirror geodev-15.md format):

```yaml
---
title: "GeoDev Meetup #N"
slug: geodev-N
date: YYYY-MM-DD
time: "HH:MM"
location: "..."
lat: 46.0445
lng: 14.5045
eventUrl: "{{LUMA_URL}}"
tags: [geodev]
---
```

Body: short intro paragraph + `## Program` with `### HH:MM — Title` headings + speaker italic + **one-paragraph** abstract per talk. **Keep abstracts short** — landing-page abstracts should be ~one paragraph; long abstracts make the event page hard to skim. (The full version lives in this repo's event README.)

## Step 4 — Banners

Copy all three banner HTMLs from the previous event:

```
cp 2026-15-meetup/banner-story.html YYYY-N-meetup/banner-story.html
cp 2026-15-meetup/banner-landscape.html YYYY-N-meetup/banner-landscape.html
cp 2026-15-meetup/banner-square.html YYYY-N-meetup/banner-square.html
```

Edit each:

* **`banner-square.html`** — minimal poster: just OSGeoSI logo + "GeoDev Slovenija" + `№ N`. Update the `№ 15` to the new number. This is the Luma cover image and the simplest to update.
* **`banner-landscape.html`** (1200×900) — left column has title/date/location/CTA; right column has the program (timestamps + talks + summaries). Update meetup number, date, location, and the three `.talk` blocks. Each talk gets a 1–2 sentence `.lede`.
* **`banner-story.html`** (1080×1920) — full portrait with title, date/location, and 3 talks with summaries. Update everything.

Design tokens are inherited from the landing-page (moss palette, paper bg, Source Serif 4 + Inter via Google Fonts). The OSGeoSI logo is inlined as SVG — leave it as-is.

Render to PNG:

```
cd scripts && node banner-to-png.js ../YYYY-N-meetup/banner-*.html
```

(One-time setup: `npm install && npx playwright install chromium`.) Each PNG lands next to its source HTML at 2× DPR (e.g. `banner-square.png` is 2160×2160). See top-level `CLAUDE.md` → "Rendering banners" for flags.

## Step 5 — Promo copy (najava.md)

Copy `2026-15-meetup/najava.md` as the template. It has six sections (LinkedIn, newsletter, Luma description, Discord/Facebook short, Twitter/X, OSGeo website blurb).

For each section, rewrite:

* Meetup number, date, location.
* Talk titles, speaker names + affiliations.
* One-sentence summary per talk (shorter than the README abstract).
* Hashtags — keep `#GeoDev #OSGeo #Slovenija #GIS` core, add talk-specific ones (#PostGIS #AI #LLM etc.) when relevant.

**Link routing convention** (observed from #15):

* **LinkedIn** post links to the landing-page event URL (`https://osgeo.si/#/dogodki/geodev-N`) — pushes traffic to the website.
* **Newsletter / Discord / Facebook / X / Luma description** all use the Luma URL directly.

Reasonable defaults if the user doesn't specify:

* Subject line for newsletter: `GeoDev #N — vabljeni na <ordinal> srečanje 🌍`
* Preview text: one-sentence digest of the talks.
* Capacity: 50 (Luma default).

## Step 6 — Hand back to the user

Report:

* Files created/edited (with paths).
* PNG dimensions confirmed by the script's output.
* Any `{{LUMA_URL}}` placeholders still in `najava.md` and the landing-page frontmatter — list the line numbers / files so they can swap once the Luma event is live.
* Suggested next actions: create Luma event with `banner-square.png` as cover, then run `Edit ... replace_all=true` to swap `{{LUMA_URL}}` for the real URL across `najava.md` and the event READMEs.

## Things NOT to do

* **Don't translate Slovenian prose to English.** Match the surrounding language.
* **Don't invent abstract text.** If the user hasn't given an abstract, ask for it — don't paraphrase a talk title into a fake abstract.
* **Don't fix typos in unrelated past README files.** Only touch the files this skill creates/edits.
* **Don't run `npm install` blindly** if `scripts/node_modules/` already exists. Check first.
* **Don't push to git or open a PR.** Stop after files are written and report — the user merges and announces.
* **Don't auto-launch the browser to "verify" the banners.** Report the PNG dimensions from the script; the user opens the PNGs themselves.
