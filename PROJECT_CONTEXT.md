# Jesus Tabernacle Display: Project Context

Last updated: 3 Oct 2026 (v0.1.1). Built by Tosin Builds.
GitHub: private repo `tosin25/jt-live-app`. Keep this file updated after every working session.
Paste this file (and SOUL.md) at the start of a new Claude chat to bring it up to speed.
SOUL.md = why and how we decide. This file = what exists and what is next. PLAN.md = the v2 front-end plan.

## 1. Goal
A desktop app for the church that listens to the pastor, shows live captions, and
automatically pops up Bible verses (KJV) when the pastor says a reference. It must
appear as a bar on top of the EasyWorship projector output. Eventually it could
replace EasyWorship and link to OBS.

## 2. Setup at the church
- One projector, driven by EasyWorship (songs, announcements, media/video feed).
- Livestream is a separate phone filming the room, so no stream overlay is needed.
- Windows laptop. Developer has Node.js installed. Only one screen for testing so far.
- Audio: planned feed from the sound desk (pastor's mic only) into a USB audio interface.
  Sound desk model: NOT YET KNOWN.

## 3. What is built (v0.1)
- Live captions with Deepgram streaming (nova-3, book names boosted as keyterms).
  Free Chrome speech engine kept as a fallback (does not work inside Electron).
- Reference parser: spoken numbers, "first/second/third" books, chapter-only,
  verse ranges (max 9 verses), "through / to / and / dash". Recent words are remembered
  ~6 seconds so a range split across speech chunks still joins up.
- Multiple Bible versions: dropdown in the header, 'Add versions' panel (download KJV or Basic English, or add a JSON file you have rights to). The version name shows on the verse, e.g. 'John 3:16 (KJV)'. Switching version re-shows the current verse.
- KJV: one-click download (thiagobodruk/bible en_kjv.json from GitHub) or load a file,
  saved in the browser's IndexedDB. 21 sample verses are built in.
- Operator window: start/stop mic, mic picker + level meter, engine choice, Deepgram key box,
  manual verse typing, auto-show toggle, list of detected verses, live preview of the output.
- Output styles: Full screen, Bottom bar, Lower third (green key).
  Themes: Classic, Royal, Sunrise, Forest, Light. Fonts: Serif, Elegant, Modern.
  Caption size: S / M / L.
- Pop-over bar (v0.2.0 retro window-card look): in Electron it is a frameless, transparent, always-on-top window placed at the bottom of
  the projector (second display if connected, else main screen). In Chrome it uses
  Document Picture-in-Picture.
- Prev / Next / Clear buttons on the bar (shown on hover), plus arrow keys and Page Up/Down
  (works with a presenter clicker). Escape clears.
- Welcome screen (logo.png + "Jesus Tabernacle"), auto-closes after 5 seconds.
- Optional default Deepgram key from config.json (gitignored, packed into the installer).
- Packaging: electron-builder produces a Windows installer (npm run build).

## 4. Architecture in one minute
- index.html is the whole app. With no hash it is the operator screen. With `#display`
  it is the output screen. The two talk through a BroadcastChannel named "verse-caption".
- main.js (Electron) opens the operator window and the overlay window. Calls to
  window.open('...#display') are intercepted and turned into the overlay bar.
- Deepgram audio: mic -> AudioContext -> ScriptProcessor -> 16 kHz PCM -> WebSocket.
  (AudioWorklet was tried and failed when opened as a local file.)
- Deepgram key: an optional default comes from config.json (gitignored, packed into the installer).
  Users can override it in the key box; overrides are saved in localStorage on that computer only.
  Anyone with the installer could extract the default key, so use a dedicated key and watch usage.
  The proper fix is a small key server that hands out short-lived keys (roadmap item 7).

## 5. Key decisions and facts
- EasyWorship has no public way to receive scripture from other software. So we overlay
  on top of its output instead of integrating with it.
- Browser-only (Chrome) cannot make a title-less always-on-top bar; Electron can. Hence Electron.
- KJV is public domain. NIV, ESV, NKJV are licensed and need checking before use.
- Song lyrics are licensed (CCLI). Do not scrape Google for lyrics.
- OBS Browser Source cannot talk to the BroadcastChannel (different browser). It would
  need a small relay server (WebSocket). OBS can also be controlled with obs-websocket.
- The installer is unsigned. Windows shows a SmartScreen warning (More info -> Run anyway).
- Each laptop needs its own one-time KJV download. The Deepgram key can be baked in via config.json (limit its usage; installer holds the key).

## 5b. Bible version licensing (checked 3 Oct 2026; not legal advice)
- Free/public domain, safe to bundle or download: KJV, Basic English (BBE). Others (ASV, WEB, YLT) can be added from a JSON file.
- NIV (Biblica): quoting up to 500 verses is allowed without permission (not a whole book, under 25% of a work); a local church using it in non-saleable media should put (NIV) after the quotation. Putting the whole NIV text inside distributed software is different and needs a licence from Biblica (biblica.com/permissions).
- API.Bible (American Bible Society) offers many licensed versions but NOT NIV via express licence; display limit 500 consecutive verses; cached text must refresh every 30 days. ESV is only through Crossway's own ESV API.
- Do NOT use random GitHub repos that host NIV/ESV database files; those are unlicensed copies.
- EasyWorship's own Bible modules are licensed to that software; do not extract them.

## 5c. Offline and slow network (v0.2.4)
- Works with NO internet: Bible text (once loaded or bundled), typing a reference, Prev/Next, highlights, the pop-over bar, all themes.
- Needs internet: live speech-to-text (Deepgram). Without it the operator can still type references.
- Slow network: "Deepgram (low data)" sends Opus audio (about 24 kbps) instead of raw audio (about 256 kbps). Slightly lower quality, much lighter. Wired connection or a dedicated phone hotspot also helps.
- Bundling: put en_kjv.json / en_bbe.json in the bibles/ folder and font files in fonts/ (see the README.txt in each), then build the installer. The app loads them at start with no download.
- Google Fonts link removed (it could stall the page on a slow network). Fonts come from the fonts/ folder or the system.
- Fully offline speech-to-text would need a local model (for example Vosk or Whisper). Not built: needs a large model download, more CPU, and testing for accuracy and delay.
- Voice commands: with a verse on screen, saying "verse 5", "chapter 4 verse 2" or "verses 5 to 7" shows that verse; optional "next verse". A spoken book name always wins. Setting: Voice commands.

## 5d. Offline speech-to-text options (researched 3 Oct 2026, nothing built or tested yet)
- Vosk: streams natively, light on the CPU, lower accuracy. Supports a limited-vocabulary mode (book names, numbers, trigger words) which could make a very reliable offline verse-reference detector.
- Whisper family (faster-whisper, whisper.cpp): more accurate, handles accents better, but not natively streaming. Whisper-Streaming reports about 3 seconds delay. Large models are slow on a laptop CPU without a GPU.
- Sherpa-ONNX: another streaming option, to evaluate.
- Plan: spike test first. Record 5 minutes of the pastor through the real audio feed, run Vosk and faster-whisper on it, compare book-name accuracy, delay and CPU use on the church laptop. Then decide on a hybrid: Deepgram when online, local detector as fallback.
- Open: church laptop specs (CPU, RAM, GPU?).

## 5e. Offline helper (Vosk), v0.3.1: built, NOT tested with real audio
- offline/vosk_refs.py (Python) listens to the microphone and sends text to the app on ws://127.0.0.1:8765. App engine: "Offline (Vosk helper)".
- Two recognisers on the same audio: captions (normal) and refs (limited to book names and number words; option --phrases limits it to every real reference in the Bible JSON, about 62,000 phrases).
- Unknown: whether Vosk treats a list of phrases as exact sequences or as a loop, and whether rare book names (Habakkuk, Zephaniah, Obadiah) are in the small model's vocabulary. The script prints missing words and has --wav --compare to test modes side by side. Decide from the results on a real recording.
- Models: vosk-model-small-en-us-0.15 (40 MB, small) or vosk-model-en-us-0.22-lgraph (128 MB, dynamic graph, more accurate).
- Church laptop: Core i7 7th gen, 8 GB RAM, 500 GB SSD (no mention of a separate graphics card). Fine for Vosk. Whisper-style models would be too slow for sub-second use on this CPU (not tested).
- Parser extras added: apostrophes ("Roman's"), "one oh five" = 105, "Psalm one nineteen" = Psalm 119.
- Known gaps: "the twenty-third Psalm" (number before book), verse ranges in the offline grammar, spoken "chapter 4 verse 2" in the offline grammar works only via numbers and the words chapter/verse.

## 6. Not yet verified (needs real-world testing)
- Whether the overlay stays above EasyWorship's output window on the projector.
- Deepgram accuracy and speed with the real sound desk feed.
- The installer build on the developer's machine (first run may need admin / Developer Mode).
- Prev/Next buttons and verse ranges with live speech.

## 7. Roadmap (agreed order)
1. Captions + scripture solid (current stage). Finish front end polish.
2. Modes: Pastor / Song, and a calm Prayer style (auto on "let us pray", off at "amen", manual override).
3. Song library with lyric matching (paste or import lyrics once, app matches the sung words
   and shows the correct line; new songs saved automatically). Check if EasyWorship can export songs.
4. Announcements, images, video files, video capture feed.
5. OBS link (scene switching, e.g. prayer scene).
6. Service planner / order of service.
7. Netlify hosting + small key server so the Deepgram key is not exposed in a public page.

## 8. Ideas and future upgrades (add yours here)
- [ ] First-run walkthrough: animated step-by-step guide when the app opens (v2).
- [ ] Prayer mode with its own look (highlight prayers).
- [ ] Solo vs choir captions (operator switch is more reliable than detection).
- [x] Fuzzy search for verses quoted without a reference (operator approves with one click). Built in v0.3.0; tune on real speech. Semantic (meaning-based) search still to do.
- [ ] Auto-update from GitHub Releases so nobody has to resend installers.
- [ ] Save settings (theme, font, style, mic) between launches.
- [ ] Mac build (must be built on a Mac).
- [ ] Code signing certificate to remove the Windows warning.
- [ ] API.Bible integration for licensed versions (needs an API.Bible key, internet, and licence terms).
- [ ] Ask Biblica about NIV permission for a church display app.
- [ ] Audio setup discussion (sound desk model, USB interface, mic routing).
- [ ] Relay server so OBS Browser Source can show the output.
- [ ] Church logo / branding on the display.
- [ ] Sermon prep list: load the verses from the sermon outline before service; one key shows the next one. Works with no speech recognition at all.
- [ ] Phone remote: a page on the church Wi-Fi (no internet needed) with Prev / Next / Clear for a second operator.
- [ ] Status strip: mic level, speech connected, Bible loaded, internet speed, with a "check everything" button.
- [ ] Service log: save the transcript and the list of verses shown after each service (notes, archive, sharing).
- [ ] Offline verse-reference detector using Vosk limited vocabulary, as a fallback when the internet is down.
- [ ] Key points: type the pastor's main points ahead of time and show them with one key.
- [ ] Follow-along: send the current verse to members' phones over the church Wi-Fi.
- [ ] Undo and "recall last verse" shortcut.
- [ ] Live-tweak panel for the display (font size, padding, colours, bar height) so the operator can fine-tune the look without a new build.
- [ ] Generate several front-end design variations from the mood board and pick one.
- [ ] Image popup: search images in the operator window and show one in a corner of the screen, click to remove (details and licensing notes in PLAN.md).
- [ ] Feedback button for operators that saves notes for the next update.

## 9. My ideas (Tosin / church: write below, with dates)
-

## 10. Front-end references (add screenshots, links, descriptions)
The v2 front-end plan, area by area, is in PLAN.md. Record references there. Use this section for quick notes. Newest first.
- (none yet)

## 11. Useful finds (articles, docs, tips from the web)
- Deepgram: browser clients can authenticate with the key as a WebSocket subprotocol; keyterms boost words like book names.
- EasyWorship: no public API for pushing scripture; accepts video/NDI inputs (so overlay or OBS compositing is the route).
- Workflow idea (YC Design Review, Eve Bouffard): keep a `soul.md` source-of-truth file so the AI has full context for every decision. We now have SOUL.md for this.
- Same video: give the AI a mood board (e.g. from Pinterest) plus the soul file, then generate many variations quickly and pick one. Use this for the display front end.
- Same video: build small live-tweak panels so you can adjust the look (sizes, colours, grain) yourself instead of re-prompting. Added to ideas below.
- Same video: "Send to an agent" feedback forms turn user requests into prompts. Possible later idea for operator feedback.
- Tip: Windows voice typing (Win+H) lets you dictate messages to Claude instead of typing.
- (add more here with the link and one line on why it matters)

## 12. Changelog
- v0.3.1: Offline helper (Vosk) and app engine, parser extras (apostrophes, "oh" as zero, Psalm one nineteen).
- v0.3.0: "Did you mean?" suggestion panel. Fuzzy book-name matching for misheard references ("have a cook 3 1" -> Habakkuk 3:1) and quoted-verse matching with no reference. Never shows automatically: the operator presses 1, 2 or 3 or clicks Show. Tested with a fake 30,000-verse Bible (index builds in about 0.3 s); thresholds still need tuning on the real KJV and real speech.
- v0.2.4: Spoken verse commands, fix for a book name right after a number being missed (back-to-back references), offline support (bundled Bibles and fonts), Deepgram low-data mode, removed render-blocking Google Fonts link.
- v0.2.3: Highlight applies on drag (no extra click), snaps to whole words, mode buttons, Whole verse button.
- v0.2.2: Overlay bar finalised as Style A: chunky block shadow, pixel-font buttons, Bar and Pill colour pickers (remembered). Taped-paper Style B saved in PLAN.md for later.
- v0.2.1: Drag-to-highlight and manual "Jesus spoke" marks on the verse, first pass of blocky shadows, macOS-colour dots, pixel-font title.
- v0.2.0: Overlay bar redesigned as a retro window card from the Pinterest references (title bar, reference pill, hard shadow, themed title colours). Electron overlay window is now transparent.
- Added SOUL.md (purpose, principles, look and feel, how Claude should work on this project).
- v0.1.2: Multiple Bible versions with a dropdown and Add versions panel (KJV, BBE, or your own file). Version shown on the verse.
- v0.1.1: Welcome screen (logo.png + "Jesus Tabernacle"), default Deepgram key from config.json, renamed app, "Built by Tosin Builds" credit, README and this file added, first push to GitHub (repo needed --force because GitHub had auto-created files).
- v0.1.0: Deepgram captions, reference parser with ranges, KJV download, themes/fonts, live preview, pop-over bar (Electron), Prev/Next/Clear on the bar, installer build setup.

## 13. Open questions
- Sound desk model and how the pastor's mic is routed?
- Final app name: currently "Jesus Tabernacle". Alternative was an RCCG name.
- Who else will install it, and do they get their own Deepgram key?
