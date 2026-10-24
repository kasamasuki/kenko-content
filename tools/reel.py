#!/usr/bin/env python3
"""Render a faceless Kenko text Reel (1080x1920, 30fps MP4) from a carousel spec.

Usage: python3 tools/reel.py specs/DATE.json posts/DATE/reel.mp4 [--no-audio]
Uses the same spec as tools/carousel.py: cover = hook, each slide = one beat, end = CTA.
Text stays inside Instagram's Reel safe zone (clear of the top bar, the right-hand buttons
and the caption area at the bottom). Each beat holds long enough to read at a glance.
Audio is a quiet synthesized placeholder beat; swap in a trending sound in the app if wanted.
"""
import json, math, os, struct, subprocess, sys, tempfile, wave
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
ML, MR = 96, 170                      # right margin clears the like/comment/share buttons
TOP, BOTTOM = 330, 1480               # keep clear of the top bar and the caption area
BG, GREEN, WHITE, GREY, DIM = "#0a0a0a", "#00FF87", "#ffffff", "#9a9a9a", "#2a2a2a"
FD = "/usr/share/fonts/opentype/inter/"
HANDLE = "@coach_chris_kenko"
TW = W - ML - MR


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def wrap(d, text, fnt):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= TW:
            cur = t
        else:
            out.append(cur); cur = w
    return out + ([cur] if cur else [])


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def fit(d, lines, name, start, min_size, max_h):
    for size in range(start, min_size - 1, -4):
        f = F(name, size)
        wrapped = [l for line in lines for l in wrap(d, line, f)]
        if len(wrapped) * size * 1.15 <= max_h:
            return f, size
    raise SystemExit(f"Too long for a Reel beat: {lines}")


def build_beats(spec):
    """Each beat: list of (text, font, colour, gap_before) blocks plus a duration in seconds."""
    d = ImageDraw.Draw(Image.new("RGB", (W, H)))
    beats = []
    hf, hs = fit(d, spec["cover"], "Inter-ExtraBold.otf", 124, 72, 700)
    blocks = [(spec.get("label", "").upper(), F("Inter-SemiBold.otf", 34), GREY, 0)]
    for i, line in enumerate(spec["cover"]):
        col = GREEN if i == len(spec["cover"]) - 1 else WHITE
        for j, l in enumerate(wrap(d, line, hf)):
            blocks.append((l, hf, col, 40 if (i == 0 and j == 0) else 0))
    beats.append((blocks, 2.4))
    for sl in spec["slides"]:
        tf, ts = fit(d, [sl["title"]], "Inter-ExtraBold.otf", 96, 64, 460)
        bf = F("Inter-Regular.otf", 54)
        blocks = []
        if sl.get("tag"):
            blocks.append((sl["tag"].upper(), F("Inter-Bold.otf", 40), GREEN, 0))
        for j, l in enumerate(wrap(d, sl["title"], tf)):
            blocks.append((l, tf, WHITE, 30 if j == 0 else 0))
        for j, l in enumerate(wrap(d, sl.get("body", ""), bf)):
            blocks.append((l, bf, GREY, 50 if j == 0 else 0))
        words = len((sl["title"] + " " + sl.get("body", "")).split())
        beats.append((blocks, round(0.9 + 0.16 * words, 2)))
    ef, es = fit(d, spec["end"], "Inter-ExtraBold.otf", 100, 64, 500)
    blocks = []
    for i, line in enumerate(spec["end"]):
        col = GREEN if i == len(spec["end"]) - 1 else WHITE
        for l in wrap(d, line, ef):
            blocks.append((l, ef, col, 0))
    blocks.append(("Follow for more.", F("Inter-Medium.otf", 42), GREY, 50))
    beats.append((blocks, 2.8))
    return beats


def layout(blocks):
    h = 0
    pos = []
    for text, f, col, gap in blocks:
        h += gap
        pos.append(h)
        h += f.size * 1.18
    if h > BOTTOM - TOP:
        raise SystemExit(f"Beat too tall: {blocks[0][0]}")
    y0 = TOP + (BOTTOM - TOP - h) / 2
    return [y0 + p for p in pos]


def frame(beats, idx, t, total_t, elapsed):
    blocks, dur = beats[idx]
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # progress bar across the top safe edge
    d.rectangle([ML, 250, W - ML, 256], fill=DIM)
    d.rectangle([ML, 250, ML + (W - 2 * ML) * min(1, (elapsed + t) / total_t), 256], fill=GREEN)
    d.text((ML, BOTTOM + 60), HANDLE, font=F("Inter-Medium.otf", 34), fill=GREEN)
    out = ease((dur - t) / 0.18) if idx < len(beats) - 1 else 1.0   # quick fade before the cut
    for k, ((text, f, col, _), y) in enumerate(zip(blocks, layout(blocks))):
        p = ease((t - 0.07 * k) / 0.35)
        if p <= 0:
            continue
        a = p * out
        rgb = tuple(int(int(col[i:i + 2], 16) * a + 10 * (1 - a)) for i in (1, 3, 5))
        d.text((ML, y + 40 * (1 - p)), text, font=f, fill=rgb)
    return img


def beat_audio(path, seconds, bpm=112):
    sr = 44100
    n = int(seconds * sr)
    spb = 60 / bpm
    samples = []
    for i in range(n):
        t = i / sr
        tb = t % spb
        kick = math.sin(2 * math.pi * (55 + 90 * math.exp(-tb * 30)) * tb) * math.exp(-tb * 9)
        th = (t + spb / 2) % spb
        hat = (((i * 1103515245 + 12345) >> 16) % 2000 / 1000 - 1) * math.exp(-th * 60) * 0.25
        v = (kick * 0.55 + hat) * 0.5
        fade = min(1, t / 0.3, (seconds - t) / 0.5)
        samples.append(int(max(-1, min(1, v * fade)) * 32767))
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(struct.pack(f"<{len(samples)}h", *samples))


def render(spec, out, audio=True):
    beats = build_beats(spec)
    total_t = sum(b[1] for b in beats)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "beat.wav")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio:
        beat_audio(wav, total_t)
        cmd += ["-i", wav, "-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
            "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    elapsed = 0.0
    for idx, (_, dur) in enumerate(beats):
        for fi in range(int(round(dur * FPS))):
            ff.stdin.write(frame(beats, idx, fi / FPS, total_t, elapsed).tobytes())
        elapsed += dur
    ff.stdin.close()
    if ff.wait():
        raise SystemExit("ffmpeg failed")
    print(f"{out}  {total_t:.1f}s, {len(beats)} beats")


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2], "--no-audio" not in sys.argv)
