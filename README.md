# Jesus Tabernacle Display

Live captions and automatic Bible verses (KJV) for church services, shown as a bar
over the projector. Built by **Tosin Builds**.

Full project notes, decisions and the ideas list are in `PROJECT_CONTEXT.md`.

## What it does today
- Live captions from the pastor's microphone (Deepgram).
- Spoken references ("John 3:16", "Romans eight twenty-eight through thirty") pop up as verses.
- Next / Previous verse buttons on the popup bar, plus arrow keys and Page Up/Down.
- Welcome screen with logo on start.
- Themes, fonts and caption sizes, with a live preview in the operator window.

## Run while developing
    npm install      (first time only)
    npm start

## Build the installer (Windows)
    npm install      (first time only)
    npm run build
The installer is created in `dist/` as "Jesus Tabernacle Setup x.y.z.exe".
Raise the "version" in package.json before each new build.
If you get a "symbolic link" error, run the terminal as administrator or turn on
Windows Developer Mode.

## First run on a new computer
1. Install with the Setup .exe (Windows shows a warning because it is unsigned:
   More info -> Run anyway).
2. Click "Download KJV" (once).
3. The Deepgram key is filled in automatically if the installer was built with a default key
   (see below). Anyone can replace it in the key box; their choice is saved on that computer only.
4. Pick the microphone, click "Pop over EasyWorship", then "Start listening".

## Default Deepgram key (optional)
Copy `config.example.json` to `config.json` and paste your key inside. The app uses it
as the default (users can still type a different one). `config.json` is in .gitignore,
so it is NOT pushed to GitHub, but it IS packed into the installer. Use a Deepgram key
with a usage limit, and do not post the installer publicly.

## Logo
Save the church logo as `logo.png` in this folder. It shows on the welcome screen.

## Edit workflow
Edit index.html (or main.js), test with `npm start`, then:
    git add .
    git commit -m "what changed"
    git push

## Files
- main.js        Electron shell: operator window + always-on-top overlay bar
- preload.js     Passes the optional default settings to the page
- logo.png       Church logo (you add this)
- config.json    Default Deepgram key (you create this; not on GitHub)
- index.html     The whole app (operator screen and display screen)
- package.json   App name, version, build settings

## Default Deepgram key (optional)
1. Copy `config.example.json` to `config.json` and paste the key in place of PASTE_YOUR_KEY_HERE.
2. `npm start` or `npm run build` will then use it as the default.
`config.json` is listed in `.gitignore`, so it is never pushed to GitHub.
The key is packed inside the installer, so anyone with the installer could extract it.
Use a dedicated key for this app and watch usage in the Deepgram console; revoke it there if needed.
