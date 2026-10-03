# Jesus Tabernacle Display: Project Context

Last updated: 3 Oct 2026. Built by Tosin Builds.
Paste this file at the start of a new Claude chat to bring it up to speed.

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
- KJV: one-click download (thiagobodruk/bible en_kjv.json from GitHub) or load a file,
  saved in the browser's IndexedDB. 21 sample verses are built in.
- Operator window: start/stop mic, mic picker + level meter, engine choice, Deepgram key box,
  manual verse typing, auto-show toggle, list of detected verses, live preview of the output.
- Output styles: Full screen, Bottom bar, Lower third (green key).
  Themes: Classic, Royal, Sunrise, Forest, Light. Fonts: Serif, Elegant, Modern.
  Caption size: S / M / L.
- Pop-over bar: in Electron it is a frameless, always-on-top window placed at the bottom of
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
- [ ] Fuzzy / semantic search for verses quoted without a reference (operator approves with one click).
- [ ] Auto-update from GitHub Releases so nobody has to resend installers.
- [ ] Save settings (theme, font, style, mic) between launches.
- [ ] Mac build (must be built on a Mac).
- [ ] Code signing certificate to remove the Windows warning.
- [ ] Other Bible translations (check licences).
- [ ] Relay server so OBS Browser Source can show the output.
- [ ] Church logo / branding on the display.

## 9. My ideas (Tosin / church: write below, with dates)
-

## 10. Open questions
- Sound desk model and how the pastor's mic is routed?
- Final app name: currently "Jesus Tabernacle". Alternative was an RCCG name.
- Who else will install it, and do they get their own Deepgram key?
