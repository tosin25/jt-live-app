#!/usr/bin/env python3
"""
Offline helper for Jesus Tabernacle Display (uses Vosk, no internet needed).

It listens to a microphone and sends what it hears to the app over a local
WebSocket (ws://127.0.0.1:8765). Two recognisers run on the same audio:
  captions : normal speech recognition, for the caption bar
  refs     : limited to Bible book names and number words, for verse references
            (--phrases = limited to every real reference in the Bible JSON, experimental)

Test on a recording first:   python vosk_refs.py --wav sample.wav --compare
Run live:                    python vosk_refs.py
"""
import argparse, array, asyncio, json, math, os, queue, sys, threading, time, wave

HERE = os.path.dirname(os.path.abspath(__file__))

# Book names as people say them, in Bible order.
SPOKEN_BOOKS = ["genesis", "exodus", "leviticus", "numbers", "deuteronomy", "joshua", "judges", "ruth",
    "first samuel", "second samuel", "first kings", "second kings", "first chronicles", "second chronicles",
    "ezra", "nehemiah", "esther", "job", "psalm", "proverbs", "ecclesiastes", "song of solomon", "isaiah",
    "jeremiah", "lamentations", "ezekiel", "daniel", "hosea", "joel", "amos", "obadiah", "jonah", "micah",
    "nahum", "habakkuk", "zephaniah", "haggai", "zechariah", "malachi", "matthew", "mark", "luke", "john",
    "acts", "romans", "first corinthians", "second corinthians", "galatians", "ephesians", "philippians",
    "colossians", "first thessalonians", "second thessalonians", "first timothy", "second timothy", "titus",
    "philemon", "hebrews", "james", "first peter", "second peter", "first john", "second john", "third john",
    "jude", "revelation"]
EXTRA_WORDS = ["psalms", "songs", "revelations", "first", "second", "third", "one", "two", "three",
    "chapter", "verse", "verses", "through", "thru", "to", "and", "dash", "next", "previous", "oh"]
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
    "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def num_to_words(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    return "one hundred" + ("" if n == 100 else " " + num_to_words(n - 100))


def words_grammar():
    """A list of single words: book names, number words and a few connecting words, plus [unk]."""
    w = set(EXTRA_WORDS) | set(ONES) | set(TENS.values()) | {"hundred"}
    for b in SPOKEN_BOOKS: w.update(b.split())
    return sorted(w) + ["[unk]"]


def phrases_grammar(bible_json):
    """Every real reference as a phrase (experimental): 'john three sixteen', 'john chapter three verse sixteen'."""
    with open(bible_json, encoding="utf-8-sig") as f: data = json.load(f)
    out = []
    for bi, book in enumerate(data):
        b = SPOKEN_BOOKS[bi]
        for ci, ch in enumerate(book["chapters"], 1):
            c = num_to_words(ci)
            out += [f"{b} {c}", f"{b} chapter {c}"]
            for v in range(1, len(ch) + 1):
                vw = num_to_words(v)
                out += [f"{b} {c} {vw}", f"{b} chapter {c} verse {vw}"]
    out += [f"verse {num_to_words(n)}" for n in range(1, 177)] + ["next verse", "previous verse", "[unk]"]
    return out


def load_model(path):
    from vosk import Model, SetLogLevel
    SetLogLevel(-1)
    if not os.path.isdir(path):
        sys.exit(f"Model folder not found: {path}\nDownload vosk-model-small-en-us-0.15 from "
                 "https://alphacephei.com/vosk/models, unzip it and rename the folder to 'model' (see README.txt).")
    return Model(path)


def check_vocab(model, words):
    missing = []
    for w in words:
        if w.startswith("["): continue
        try:
            if model.vosk_model_find_word(w) < 0: missing.append(w)
        except AttributeError:
            return None
    return missing


def make_recognisers(model, rate, mode, phrases_file):
    from vosk import KaldiRecognizer
    recs = {}
    if mode in ("both", "free"):
        recs["caption"] = KaldiRecognizer(model, rate)
    if mode in ("both", "words"):
        grammar = phrases_grammar(phrases_file) if phrases_file else words_grammar()
        recs["refs"] = KaldiRecognizer(model, rate, json.dumps(grammar))
    return recs


def run_wav(args):
    model = load_model(args.model)
    with wave.open(args.wav, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in (8000, 16000, 44100, 48000):
            sys.exit("The WAV must be mono, 16-bit. Convert with:  ffmpeg -i input.mp4 -ar 16000 -ac 1 sample.wav")
        rate, secs = wf.getframerate(), wf.getnframes() / wf.getframerate()
        pcm = wf.readframes(wf.getnframes())
    miss = check_vocab(model, words_grammar())
    print("Book/number words missing from this model:", "(check not available)" if miss is None else (miss or "none"))
    modes = ["free", "words"] + (["phrases"] if args.phrases else []) if args.compare else [args.mode]
    for m in modes:
        recs = make_recognisers(model, rate, "words" if m == "phrases" else m, args.phrases if m == "phrases" else None)
        t0, finals = time.time(), {k: [] for k in recs}
        for i in range(0, len(pcm), 8000):
            chunk = pcm[i:i + 8000]
            for k, r in recs.items():
                if r.AcceptWaveform(chunk): finals[k].append(json.loads(r.Result()).get("text", ""))
        for k, r in recs.items(): finals[k].append(json.loads(r.FinalResult()).get("text", ""))
        el = time.time() - t0
        print(f"\n=== mode: {m}   time {el:.1f}s for {secs:.1f}s of audio (speed {el / secs:.2f}x, under 1.0 is faster than real time)")
        for k, v in finals.items(): print(f"[{k}] " + " | ".join(t for t in v if t))


def list_devices():
    import sounddevice as sd
    print(sd.query_devices())


def run_live(args):
    import sounddevice as sd, websockets
    model = load_model(args.model)
    miss = check_vocab(model, words_grammar())
    if miss: print("Warning: these words are not in the model and will not be recognised:", ", ".join(miss))
    rate = 16000
    recs = make_recognisers(model, rate, args.mode, args.phrases)
    q, stop = queue.Queue(), threading.Event()
    clients, last = set(), {}
    loop = asyncio.new_event_loop()

    def send(msg):
        data = json.dumps(msg)
        for c in list(clients):
            try: asyncio.run_coroutine_threadsafe(c.send(data), loop)
            except Exception: pass

    def worker():
        lvl_t = 0
        while not stop.is_set():
            try: data = q.get(timeout=0.2)
            except queue.Empty: continue
            now = time.time()
            if now - lvl_t > 0.1:
                a = array.array("h", data); lvl_t = now
                send({"type": "level", "v": math.sqrt(sum(x * x for x in a) / max(1, len(a))) / 32768})
            for kind, r in recs.items():
                if r.AcceptWaveform(data):
                    t = json.loads(r.Result()).get("text", "")
                    if t: send({"kind": kind, "type": "final", "text": t})
                    last[kind] = ""
                else:
                    t = json.loads(r.PartialResult()).get("partial", "")
                    if t and t != last.get(kind): last[kind] = t; send({"kind": kind, "type": "partial", "text": t})

    def callback(indata, frames, t, status): q.put(bytes(indata))

    async def handler(ws, path=None):
        clients.add(ws)
        try: await ws.wait_closed()
        finally: clients.discard(ws)

    async def serve():
        async with websockets.serve(handler, "127.0.0.1", args.port):
            print(f"Offline helper running on ws://127.0.0.1:{args.port}. In the app choose 'Offline (Vosk helper)' and press Start listening.")
            await asyncio.Event().wait()

    threading.Thread(target=worker, daemon=True).start()
    with sd.RawInputStream(samplerate=rate, blocksize=2000, device=args.device, dtype="int16", channels=1, callback=callback):
        asyncio.set_event_loop(loop)
        try: loop.run_until_complete(serve())
        except KeyboardInterrupt: pass
    stop.set()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default=os.path.join(HERE, "model"))
    p.add_argument("--mode", choices=["both", "free", "words"], default="both")
    p.add_argument("--phrases", metavar="BIBLE_JSON", help="experimental: limit 'refs' to every real reference in this Bible JSON (for example ../bibles/en_kjv.json)")
    p.add_argument("--device", type=int, help="microphone number from --list-devices")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--wav", help="test on a recording instead of the microphone")
    p.add_argument("--compare", action="store_true", help="with --wav: try free, words (and phrases if given) side by side")
    p.add_argument("--list-devices", action="store_true")
    p.add_argument("--selftest", action="store_true", help="print the grammar sizes and exit (no model needed)")
    a = p.parse_args()
    if a.selftest:
        g = words_grammar(); print("words grammar:", len(g), "entries"); print("sample:", g[:12], "...")
        if a.phrases: ph = phrases_grammar(a.phrases); print("phrases grammar:", len(ph), "phrases; e.g.", ph[:3])
        print("105 =", num_to_words(105), "| 16 =", num_to_words(16), "| 28 =", num_to_words(28)); return
    if a.list_devices: return list_devices()
    return run_wav(a) if a.wav else run_live(a)


if __name__ == "__main__":
    main()
