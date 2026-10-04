# PLAN.md: Version 2 plan (front end and new features)

Owner: Tosin Builds. Started 3 Oct 2026. Companion files: SOUL.md (why), PROJECT_CONTEXT.md (what exists).
Add references and ideas here any time. Claude reads this before doing any v2 design work.

## How we design (the workflow)
1. Tosin saves ideas on Pinterest, one board per area below, and shares screenshots or links.
   (Screenshots are the most reliable. Claude may not be able to open private boards.)
2. Claude reads SOUL.md + this file + the references for that area.
3. Claude proposes 2 to 3 variations, Tosin picks one.
4. We add a small live-tweak panel where it helps (sizes, colours, spacing) so the look can be fine-tuned without a rebuild.
5. Tested on the real projector/screen before it goes into a Sunday service.

## Order of work
Original order: operator window, congregation display, overlay bar, onboarding, brand, accessibility.
Recommended order (a few changes, with reasons):
1. **Brand / RCCG** (small, decide first): logo, colours, fonts. Everything else uses these, so deciding first avoids redoing screens.
2. **Overlay bar and congregation display**: what people actually see and where Sunday risk is highest. The bar is the pop-over over EasyWorship; the congregation display is the full-screen / lower-third output. They share one look.
3. **Operator window**: the control screen for volunteers.
4. **Setup / onboarding**: the first-run guide and checks.
5. **Accessibility**: rules apply from step 1 (see below), plus a full check at the end. Not left until last.

## Area 1: Brand / RCCG
- Goal: it looks like it belongs to Jesus Tabernacle (RCCG), not a generic tool.
- Decide: logo placement (welcome screen now; display bar? corner?), colour palette, heading and verse fonts, icon for the installer (needs an .ico).
- Pinterest board: "JT - Brand RCCG"
- References: (none yet)

## Area 2a: Overlay bar (the pop-over over EasyWorship)
- Goal: verse text is huge and clear in a thin bar; captions shown when no verse is up; never blocks the key content of the EasyWorship slide.
- Decide: bar height, position (bottom), background (solid, gradient, translucent), verse and reference layout, how the version label (KJV) looks, caption style, how Prev/Next/Clear appear on hover, animation on verse change.
- Pinterest board: "JT - Overlay bar"
- References received 3 Oct 2026 (6 images): retro / neo-brutalist "window" cards.
  Common traits: window frame with a coloured title bar and dots (or square buttons), thick dark outline,
  hard offset shadow (no blur), rounded corners, pastel colours (powder blue, lilac, periwinkle), cream or white card,
  highlight "pills" behind key words (green, yellow, pink), chunky wide sans headings, yellow button with an arrow.
- Design decisions (v0.2.0, built):
  - The bar is a window card: title bar with three dots and "Jesus Tabernacle" (plus logo.png if present).
  - The scripture reference sits in a yellow pill on the title bar, like the highlight pills in the references.
  - Verse text is dark ink on cream (high contrast), in the chosen verse font; captions use the same card.
  - Prev / Next / Clear are yellow buttons with a hard shadow, shown on hover at the bottom right.
  - Themes now change the title bar colour: Classic (powder blue), Royal (periwinkle), Sunrise (peach), Forest (mint), Light (lilac).
  - In the desktop app the overlay window is transparent, so the card floats over EasyWorship with no black box around it.
  - Heading font: Syne (needs internet the first time; falls back to a system font offline. Bundle the font later).
- Not yet done: pixel/retro buttons (from reference 1), highlight pills on caption words (reference 3), gingham/grid backdrops (only possible on the full-screen display, not the transparent bar), sunburst background (reference 4).
- Tosin to confirm: colours, whether to keep the dots, title bar text, and bar height.

## Design opinions and decisions (3 Oct 2026)
- Highlight pills (reference 3): YES for scripture emphasis, NO for automatic caption highlighting.
  Operator selects a phrase in the verse (for example "whosoever") and it shows as a pill on the display. One highlight colour only, dark text on the pill for contrast.
  Reason: pastors stress words; auto-highlighting captions flickers and distracts. Not built yet.
- Emojis and short images: YES, but operator-triggered and from an approved set, never automatic from speech (a wrong emoji in prayer is worse than none).
  Plan: a church media folder (PNG with transparent background, small GIF/short clip) plus a small emoji picker, shown as a sticker in a corner of the card, click to remove, included in Clear.
  Local files first (works offline, licensing under our control). Online image search comes later (see the image popup feature).
  Keep motion gentle: no flashing, respect reduce motion.
- Hard blocky shadow (reference 4): YES. Keep it on the card, reference pill and buttons only. It stays crisp on a projector where soft shadows wash out, and it separates the card from busy EasyWorship slides. Reuse the same shadow on the operator window, welcome screen and onboarding for a consistent brand. Do not put it on every element.
- Suggested build order: 1) emphasis highlight, 2) sticker/emoji popup from a local folder, 3) shadow style across other screens.

## Area 2b: Congregation display (full screen and lower third)
- Goal: calm and reverent; readable from the back row.
- Decide: themes (keep or replace the current five), backgrounds (colour, gradient, subtle motion or stills), verse typography, reference placement, caption look.
- Pinterest board: "JT - Congregation display"
- References: (none yet)

## Area 3: Operator window
- Goal: a volunteer understands it in 5 minutes. Fewer visible controls, clear status.
- Ideas: group controls (Audio, Bible, Display), a big status strip (Listening / Not listening, Deepgram connected), larger Prev/Next/Clear, hide advanced settings, clearer detected-verses list, a panic "Clear everything" button.
- Pinterest board: "JT - Operator window"
- References: (none yet)

## Area 4: Setup / onboarding
- Goal: a new laptop is ready in minutes with no help.
- Ideas: animated first-run walkthrough (welcome, add Bible version, enter or confirm key, pick mic and see the level move, test a verse, place the pop-over bar); a "check everything" button (mic, internet, Deepgram, Bible loaded, projector found); skip option; replay from a Help button.
- Pinterest board: "JT - Onboarding"
- References: (none yet)

## Area 5: Accessibility
Applied to every area from the start, then checked at the end.
**Congregation display**
- Strong contrast between text and background (aim well above the minimum 4.5:1; projectors wash colours out).
- Large minimum text size readable from the back row; a Large text option.
- Plain, sturdy fonts (avoid thin or ornate fonts for verses); optional dyslexia-friendly font.
- Safe margins so the projector does not cut off text at the edges.
- No flashing; gentle fades only; respect "reduce motion".
- Never rely on colour alone to show meaning (for example, prayer mode should also differ in layout or label).
- Colour-blind-safe palettes; a High contrast theme.
- Captions for hearing-impaired members: keep them accurate, steady and unhurried, not jumping around.
**Operator window**
- Everything usable by keyboard, with a clearly visible focus outline.
- Screen-reader labels on buttons and status messages that announce changes.
- Big click targets (works on touch screens), text that scales.
- Plain-language errors that say what to do next.
- A visible "Clear" at all times.
**Later**
- Captions sent to phones or tablets (QR code) so members can read along privately.
- Other languages for captions.
- Pinterest board: "JT - Accessibility"
- References: (none yet)

## V2 feature: Image popup (search and show a picture)
Idea (Tosin): in the operator window, a quick image search. When the pastor mentions something, the operator searches, scrolls through results, clicks one, and it pops up in a corner of the congregation screen. Click it again to remove.
- Where: a search box and scrolling thumbnail strip in the operator window; the image appears in a corner of the overlay or display, with a small close action.
- Operator always previews before showing; one click to remove; included in the panic Clear.
- Image source (to decide). Notes:
  - Ordinary Google or Pinterest images are mostly copyrighted, and automatically pulling them into the app is risky and may break their terms.
  - Safer sources with free-to-use licences and official search APIs: Unsplash, Pexels, Pixabay, Wikimedia Commons. Needs internet and a free API key.
  - Pinterest could be used as the church's own saved board of approved images rather than a live search (to confirm what "connected to Pin" should mean).
  - Safe search on, and no auto-show: a wrong image on screen mid-service is a bigger risk than a wrong verse.
- Status: idea only. Decide the source before building.

## Other v2 ideas (from PROJECT_CONTEXT.md)
Prayer mode look, Pastor/Song modes, song library with lyric matching, OBS link, service planner, API.Bible versions, auto-update. See PROJECT_CONTEXT.md sections 7 and 8.

## Open questions
- What exactly should "connected to Pin" mean for the image search (Pinterest board vs search)?
- Brand colours and fonts for Jesus Tabernacle?
- Should the image popup also appear on the livestream phone feed? (Probably not.)

## Built in v0.2.1 (3 Oct 2026)
- Drag-to-highlight: in the operator "On display now" panel, drag across words and click Highlight (yellow pill on the display).
- "Jesus spoke": same idea with a soft rose pill (dark red text, readable on any background). With nothing selected it marks the whole verse. Manual for now.
- Future: automatic words-of-Jesus (red letter) needs a red-letter Bible data file. KJV downloads we use do not include it. Find a licensed or public-domain red-letter KJV dataset, then mark those ranges automatically.
- First pass of the hard blocky shadow on buttons, the live panel, the preview and the welcome button.
- Title bar dots now use the macOS colours (red, yellow, green). Title uses the pixel font Silkscreen.
- Fonts (Syne, Silkscreen) load from Google Fonts. Offline they fall back to plain fonts. Todo: bundle the font files in the app.
