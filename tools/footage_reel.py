#!/usr/bin/env python3
"""Render a footage Kenko Reel (1080x1920, 30fps MP4): real clips with one short line of text each.

Usage: python3 tools/footage_reel.py specs/SLOT.json posts/SLOT/reel.mp4 [--no-audio]

Spec:
{
  "label": "Movement of the week",              optional small grey kicker on the first beat
  "beats": [
    {"clip": "footage/chalk-hands.mp4", "start": 1.0, "dur": 2.2,
     "text": ["Coach says", "last round."]},    1 to 3 short lines, last line green, ~6 words max
    {"clip": "footage/rower-monitor.mp4", "dur": 2.0,
     "text": ["It is not", "the last round."]},
    ...
  ],
  "end": ["Tag the one who", "believed it."]       optional end text, shown over the last beat's clip
}
- Clips live in footage/ (any phone video; it is scaled and centre-cropped to 9:16).
  "start" is seconds into the clip (default 0), "dur" how long the beat holds (default 2.0).
  A clip shorter than start+dur is looped.
- Faceless: clips show equipment, hands, feet, the whiteboard, the room. No faces.
- Text sits in Instagram's Reel safe zone over a soft dark band so it reads on any footage.
  Keep lines short: viewers should never need to pause to read.
- Total length 7 to 25 seconds. Brand: white, #00FF87, Inter. No emojis, hashtags or em dashes.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import beat_audio  # same placeholder beat as the text Reels

W, H, FPS = 1080, 1920, 30
ML, MR = 96, 170
TOP, BOTTOM = 330, 1480
GREEN, WHITE, GREY = (0, 255, 135), (255, 255, 255), (200, 200, 200)
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


def overlay(lines, label=None, cta=False):
    """Transparent 1080x1920 PNG: dark band + text, centred in the safe zone."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for size in range(118, 63, -4):
        f = F("Inter-ExtraBold.otf", size)
        rows = [(l, i) for i, line in enumerate(lines) for l in wrap(d, line, f)]
        if len(rows) * size * 1.15 <= 620:
            break
    else:
        raise SystemExit(f"Too long for a footage beat: {lines}")
    lab = F("Inter-SemiBold.otf", 36)
    h = len(rows) * size * 1.15 + (70 if label else 0) + (80 if cta else 0)
    y0 = TOP + (BOTTOM - TOP - h) / 2 + 120          # sits a little low, like native captions
    # soft dark band behind the text
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).rectangle([0, y0 - 90, W, y0 + h + 90], fill=165)
    band = band.filter(ImageFilter.GaussianBlur(60))
    img = Image.composite(Image.new("RGBA", (W, H), (10, 10, 10, 255)), Image.new("RGBA", (W, H), (0, 0, 0, 0)), band)
    d = ImageDraw.Draw(img)
    y = y0
    if label:
        d.text((ML, y), label.upper(), font=lab, fill=GREY); y += 70
    for l, i in rows:
        d.text((ML, y), l, font=f, fill=GREEN if i == len(lines) - 1 else WHITE,
               stroke_width=2, stroke_fill=(10, 10, 10))
        y += size * 1.15
    if cta:
        d.text((ML, y + 30), "Follow for more.", font=F("Inter-Medium.otf", 44), fill=GREY)
    d.text((ML, BOTTOM + 60), HANDLE, font=F("Inter-Medium.otf", 34), fill=GREEN,
           stroke_width=2, stroke_fill=(10, 10, 10))
    return img


def clip_len(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def render(spec, out, audio=True):
    beats = spec["beats"]
    if spec.get("end"):
        last = dict(beats[-1]); last["text"] = spec["end"]; last["cta"] = True
        last["start"] = last.get("start", 0) + last.get("dur", 2.0)
        last["dur"] = 2.6
        beats = beats + [last]
    total = sum(b.get("dur", 2.0) for b in beats)
    if not 7 <= total <= 25:
        raise SystemExit(f"Reel is {total:.1f}s; keep it 7 to 25 seconds")
    tmp = tempfile.mkdtemp()
    parts = []
    for i, b in enumerate(beats):
        if not os.path.exists(b["clip"]):
            raise SystemExit(f"Missing clip: {b['clip']}")
        dur, start = b.get("dur", 2.0), b.get("start", 0.0)
        png = os.path.join(tmp, f"o{i}.png")
        overlay(b["text"], spec.get("label") if i == 0 else None, b.get("cta", False)).save(png)
        part = os.path.join(tmp, f"p{i}.mp4")
        loop = ["-stream_loop", "-1"] if clip_len(b["clip"]) < start + dur else []
        fade = f",fade=t=in:st=0:d=0.12" if i else ""
        subprocess.run(["ffmpeg", "-v", "error", "-y", *loop, "-ss", str(start), "-i", b["clip"], "-loop", "1", "-i", png,
                        "-filter_complex",
                        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
                        f"eq=brightness=-0.06:saturation=0.85,setsar=1{fade}[v];"
                        f"[1:v]fade=t=in:st=0:d=0.2:alpha=1[t];[v][t]overlay=0:0:shortest=1,format=yuv420p",
                        "-t", str(dur), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", part], check=True)
        parts.append(part)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst]
    if audio:
        wav = os.path.join(tmp, "a.wav"); beat_audio(wav, total)
        cmd += ["-i", wav, "-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += ["-c:v", "copy", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(f"{out}  {total:.1f}s, {len(beats)} beats")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 2:
        sys.exit(__doc__)
    render(json.load(open(a[0])), a[1], audio="--no-audio" not in sys.argv)
