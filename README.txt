OFFLINE HELPER (Vosk): speech recognition with no internet.  Experimental: test it before relying on it.

One-time setup (needs internet for about 50 MB)
1. Install Python 3.11 or 3.12 from python.org. Tick "Add python.exe to PATH" in the installer.
2. Open Command Prompt in this "offline" folder (click the folder's address bar, type cmd, Enter).
3. Run:  pip install vosk sounddevice websockets
4. Download the small English model (about 40 MB):
   https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
   Unzip it, and rename the unzipped folder to  model  so you have  offline\model
   (A bigger, more accurate model is vosk-model-en-us-0.22-lgraph, about 128 MB. Same steps.)

Test on a recording BEFORE using it live
1. Record a minute or two of the pastor (or yourself reading references) and save as WAV:
     ffmpeg -i recording.mp4 -ar 16000 -ac 1 sample.wav
2. Run:  python vosk_refs.py --wav sample.wav --compare
   It prints what each mode heard, how long it took, and any book names the model does not know.
   Experimental mode using every real Bible reference:
     python vosk_refs.py --wav sample.wav --compare --phrases ..\bibles\en_kjv.json
3. Send me what it printed.

Run live
1. List microphones:  python vosk_refs.py --list-devices   (then add  --device NUMBER  below if needed)
2. Start:  python vosk_refs.py     (or double-click start-offline.bat)
3. In the app set Speech engine to "Offline (Vosk helper)" and press Start listening.
Leave the helper window open while you use the app.
