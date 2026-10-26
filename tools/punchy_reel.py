#!/usr/bin/env python3
"""Render a short, punchy Kenko text Reel (1080x1920, 30fps MP4). Very little reading per frame.

Usage: python3 tools/punchy_reel.py specs/SLOT.json posts/SLOT/reel.mp4 [--no-audio]

Every spec has "format" plus that format's fields. Text lists: last line is green.
Optional on all: "label" (small grey kicker on the first frame).

1. oneliner  Setup, then punchline. No end card, so it loops straight back to the setup.
   {"format": "oneliner", "setup": ["Coach says:", "\"Last round.\""], "punch": ["It is not", "the last round."],
    "setup_dur": 2.0, "punch_dur": 3.0}
2. timer     A big green clock with one thought per step.
   {"format": "timer", "hook": ["20 minute AMRAP.", "Minute by minute."],
    "steps": [{"clock": "0:00", "text": "Smooth. Easy."}, ...], "step_dur": 1.5, "end": ["Tag the one", "who sprints at 19:00."]}
3. flash     Items flash fast; viewers pause on one or screenshot.
   {"format": "flash", "hook": ["Pause on a random frame.", "That's your gym habit."],
    "items": ["Counts generously.", ...], "item_dur": 0.6, "end": ["Tag who", "you got."]}
4. counter   A big number ticks to each value.
   {"format": "counter", "hook": ["Your 500m split.", "Round 1 vs round 5."], "unit": "/500m", "time": true,
    "stages": [{"label": "Round 1", "value": 112}, ...], "punch": ["Pace round one", "like round five."]}
   With "time": true values are seconds shown as m:ss; otherwise whole numbers.
5. versus    This or that, split screen.
   {"format": "versus", "hook": ["Pick one.", "No thinking."], "pairs": [["5am", "6pm"], ...],
    "pair_dur": 1.4, "end": ["Tag the one", "who picked burpees."]}
Keep the total 5 to 25 seconds. Brand: #0a0a0a, white, #00FF87, Inter. No emojis, hashtags or em dashes.
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from reel import beat_audio, ease

W, H, FPS = 1080, 1920, 30
ML, MR = 96, 170
TOP, BOTTOM = 330, 1480
BG, GREEN, WHITE, GREY, DIM = (10, 10, 10), (0, 255, 135), (255, 255, 255), (154, 154, 154), (42, 42, 42)
FD = "/usr/share/fonts/opentype/inter/"
HANDLE = "@coach_chris_kenko"
TW = W - ML - MR


def F(name, size):
    return ImageFont.truetype(FD + name, size)


_d = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def wrap(text, fnt, width=TW):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if _d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            out.append(cur); cur = w
    return out + ([cur] if cur else [])


def fit(lines, start, low, max_h, name="Inter-ExtraBold.otf", width=TW):
    for size in range(start, low - 1, -4):
        f = F(name, size)
        rows = [(l, i) for i, line in enumerate(lines) for l in wrap(line, f, width)]
        if len(rows) * size * 1.15 <= max_h:
            return f, rows
    raise SystemExit(f"Too long: {lines}")


def mix(col, a):
    return tuple(int(c * a + b * (1 - a)) for c, b in zip(col, BG))


def base():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((ML, BOTTOM + 60), HANDLE, font=F("Inter-Medium.otf", 34), fill=GREEN)
    return img, d


def block(d, lines, t, y=None, start=128, low=72, max_h=760, label=None, cta=False, anim=True):
    """Draw a stack of big lines (last green), vertically centred unless y is given."""
    f, rows = fit(lines, start, low, max_h)
    lh = f.size * 1.15
    h = len(rows) * lh + (70 if label else 0) + (90 if cta else 0)
    y = TOP + (BOTTOM - TOP - h) / 2 if y is None else y
    if label:
        d.text((ML, y), label.upper(), font=F("Inter-SemiBold.otf", 36), fill=mix(GREY, ease(t / 0.3) if anim else 1)); y += 70
    for k, (l, i) in enumerate(rows):
        p = ease((t - 0.06 * k) / 0.3) if anim else 1.0
        d.text((ML, y + 36 * (1 - p)), l, font=f, fill=mix(GREEN if i == len(lines) - 1 else WHITE, p))
        y += lh
    if cta:
        d.text((ML, y + 40), "Follow for more.", font=F("Inter-Medium.otf", 44), fill=mix(GREY, ease((t - 0.3) / 0.3)))


# Each scene: (duration, draw(t) -> Image)

def scene_text(lines, dur, label=None, cta=False, start=128):
    def draw(t):
        img, d = base(); block(d, lines, t, label=label, cta=cta, start=start); return img
    return (dur, draw)


def oneliner(s):
    return [scene_text(s["setup"], s.get("setup_dur", 2.0), s.get("label"), start=140),
            scene_text(s["punch"], s.get("punch_dur", 3.0), start=140)]


def timer(s):
    sc = [scene_text(s["hook"], 2.0, s.get("label"))]
    cf, tf = F("Inter-ExtraBold.otf", 250), F("Inter-ExtraBold.otf", 92)
    for st in s["steps"]:
        def draw(t, st=st):
            img, d = base()
            p = ease(t / 0.25)
            d.text((ML, 520 - 30 * (1 - p)), st["clock"], font=cf, fill=mix(GREEN, p))
            y = 860
            for k, l in enumerate(wrap(st["text"], tf)):
                q = ease((t - 0.1 - 0.05 * k) / 0.3)
                d.text((ML, y + 30 * (1 - q)), l, font=tf, fill=mix(WHITE, q)); y += 106
            return img
        sc.append((s.get("step_dur", 1.5), draw))
    if s.get("end"):
        sc.append(scene_text(s["end"], 2.6, cta=True, start=110))
    return sc


def flash(s):
    sc = [scene_text(s["hook"], 2.2, s.get("label"))]
    n = len(s["items"])
    for i, item in enumerate(s["items"]):
        def draw(t, i=i, item=item):
            img, d = base()
            d.text((ML, 420), f"{i + 1:02d} / {n:02d}", font=F("Inter-Bold.otf", 44), fill=GREEN)
            block(d, [item], t, start=130, anim=False)
            return img
        sc.append((s.get("item_dur", 0.6), draw))
    if s.get("end"):
        sc.append(scene_text(s["end"], 2.6, cta=True, start=110))
    return sc


def counter(s):
    sc = [scene_text(s["hook"], 2.0, s.get("label"))]
    fmt = (lambda v: f"{int(v) // 60}:{int(v) % 60:02d}") if s.get("time") else (lambda v: f"{int(round(v))}")
    nf, lf, uf = F("Inter-ExtraBold.otf", 300), F("Inter-Bold.otf", 56), F("Inter-SemiBold.otf", 56)
    prev = 0 if not s.get("time") else max(0, s["stages"][0]["value"] - 30)
    for st in s["stages"]:
        def draw(t, st=st, a=prev):
            img, d = base()
            v = a + (st["value"] - a) * ease(t / 0.8)
            d.text((ML, 560), st["label"].upper(), font=lf, fill=GREY)
            txt = fmt(v)
            d.text((ML, 660), txt, font=nf, fill=GREEN if st is s["stages"][-1] else WHITE)
            if s.get("unit"):
                d.text((ML + _d.textlength(txt, font=nf) + 20, 860), s["unit"], font=uf, fill=GREY)
            return img
        sc.append((s.get("stage_dur", 1.8), draw))
        prev = st["value"]
    sc.append(scene_text(s["punch"], 2.8, cta=True, start=110))
    return sc


def versus(s):
    sc = [scene_text(s["hook"], 2.0, s.get("label"))]
    pf = F("Inter-ExtraBold.otf", 150)
    mid = (TOP + BOTTOM) // 2
    for a, b in s["pairs"]:
        def draw(t, a=a, b=b):
            img, d = base()
            p, q = ease(t / 0.25), ease((t - 0.15) / 0.25)
            fa, ra = fit([a], 150, 80, 340, width=TW)
            fb, rb = fit([b], 150, 80, 340, width=TW)
            ya = mid - 70 - len(ra) * fa.size * 1.15
            for l, _ in ra:
                d.text((ML - 40 * (1 - p), ya), l, font=fa, fill=mix(WHITE, p)); ya += fa.size * 1.15
            d.rectangle([ML, mid - 3, W - MR, mid + 3], fill=DIM)
            vs = F("Inter-Bold.otf", 44)
            d.rectangle([ML, mid - 36, ML + 110, mid + 36], fill=BG)
            d.text((ML, mid - 28), "VS", font=vs, fill=GREY)
            yb = mid + 70
            for l, _ in rb:
                d.text((ML + 40 * (1 - q), yb), l, font=fb, fill=mix(GREEN, q)); yb += fb.size * 1.15
            return img
        sc.append((s.get("pair_dur", 1.4), draw))
    if s.get("end"):
        sc.append(scene_text(s["end"], 2.6, cta=True, start=110))
    return sc


FORMATS = {"oneliner": oneliner, "timer": timer, "flash": flash, "counter": counter, "versus": versus}


def render(spec, out, audio=True):
    scenes = FORMATS[spec["format"]](spec)
    total = sum(dur for dur, _ in scenes)
    if not 5 <= total <= 25:
        raise SystemExit(f"Reel is {total:.1f}s; keep it 5 to 25 seconds")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    tmp = tempfile.mkdtemp()
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio:
        wav = os.path.join(tmp, "a.wav"); beat_audio(wav, total)
        cmd += ["-i", wav, "-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for dur, draw in scenes:
        for fi in range(int(round(dur * FPS))):
            p.stdin.write(draw(fi / FPS).tobytes())
    p.stdin.close()
    if p.wait():
        raise SystemExit("ffmpeg failed")
    print(f"{out}  {total:.1f}s, {len(scenes)} scenes")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(a) != 2:
        sys.exit(__doc__)
    render(json.load(open(a[0])), a[1], audio="--no-audio" not in sys.argv)
