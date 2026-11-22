#!/usr/bin/env python3
"""Render a Kenko single-image text meme (1080x1350 PNG) from a JSON spec.

Usage: python3 tools/meme.py specs/DATE.json posts/DATE/01.png

Added 2026-11-16 for the 4pm meme-card experiment (see ops/PLAYBOOK.md Change log).
Modelled on Chris's best static memes: one community in-joke, read in 2 seconds, sent to a
training partner. Deliberately NOT the dark coaching look, so it reads as a meme, not a lesson.

Spec:
{
  "lines": ["Rich in community.", "Poor in cartilage."],   1 to 4 short lines, 25 words max in total
  "tag": "Which one are you?"                               optional small last line (question or tag nudge)
}
Each line is its own short paragraph; the last one is the punchline.

Scene cards (added 2026-11-23, weekly review experiment): add "scene" to draw one gym object under
the setup lines, so the punchline is a picture, not a sentence. Objects only, never people.
  "lines": ["Coach: \"Quick finisher.\""],                    1 to 2 setup lines (14 words max)
  "scene": one of
    {"type": "whiteboard", "title": "FRAN", "rows": ["Sam 3:42", "Jess 4:15", "You CAP +3"],
     "small": [2], "circle": 2}              marker handwriting; "small" rows written tiny, "circle" ringed in red
    {"type": "clock", "time": "12:00", "label": "QUICK FINISHER"}
                                             gym interval clock, red seven-segment digits (0-9 : + - .)
    {"type": "monitor", "rows": [["1:38", "/500m"], ["34", "s/m"], ["0:47", "time"]], "label": "JUST ROW"}
                                             rower monitor LCD, 1 to 3 readouts (digits as above)
  "tag": "Tag the warm-up guy."
Brand: no emojis, hashtags or em dashes, no people, no logos.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1080, 1350, 104
BG, INK, GREY, ACCENT = "#f3f1ec", "#0a0a0a", "#77736c", "#00b862"
FD = "/usr/share/fonts/opentype/inter/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def wrap(d, text, f, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            out.append(cur); cur = w
    return out + ([cur] if cur else [])


def check(spec):
    lines = spec.get("lines") or []
    if not 1 <= len(lines) <= 4:
        raise SystemExit("Use 1 to 4 lines.")
    sc = spec.get("scene") or {}
    extra = [sc.get("title", ""), sc.get("label", ""), sc.get("time", "")] + [r if isinstance(r, str) else " ".join(r) for r in sc.get("rows") or []]
    text = " ".join(lines + [spec.get("tag", "")] + extra)
    if len(" ".join(lines + [spec.get("tag", "")]).split()) > 25:
        raise SystemExit("Too long for a meme card: 25 words max.")
    if "#" in text or "—" in text or re.search("[\U0001F300-\U0001FAFF☀-➿]", text):
        raise SystemExit("No hashtags, emojis or em dashes.")


def render(spec, out):
    check(spec)
    if spec.get("scene"):
        return render_scene(spec, out)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    width = W - 2 * M
    lines = spec["lines"]
    for size in range(88, 51, -4):
        f = F("Inter-ExtraBold.otf", size)
        rows = [wrap(d, l, f, width) for l in lines]
        lh = int(size * 1.16)
        gap = int(size * 0.55) if len(lines) > 1 else 0
        total = sum(len(r) for r in rows) * lh + gap * (len(rows) - 1)
        if total <= H - 2 * M - 220:
            break
    tag_f = F("Inter-SemiBold.otf", 46)
    y = (H - total - (110 if spec.get("tag") else 0)) // 2 - 20
    for i, r in enumerate(rows):
        if i:
            y += gap
        for row in r:
            d.text((M, y), row, font=f, fill=INK)
            y += lh
    if spec.get("tag"):
        y += 56
        d.rectangle([M, y + 6, M + 10, y + 52], fill=ACCENT)
        d.text((M + 34, y), spec["tag"], font=tag_f, fill=GREY)
    d.text((M, H - M - 30), "@coach_chris_kenko", font=F("Inter-Medium.otf", 34), fill=GREY)
    img.save(out)


MARKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "PermanentMarker-Regular.ttf")
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc",
       "7": "abc", "8": "abcdefg", "9": "abcdfg", "-": "g", "+": "g|", " ": ""}


def seg_width(text, h):
    w = h * 0.52
    return sum(h * 0.2 if c in ":." else w + h * 0.14 for c in text)


def seg_text(d, x, y, text, h, on, off=None):
    """Seven-segment digits, top-left at (x, y), digit height h."""
    w, t = h * 0.52, max(4, h * 0.11)
    for c in text:
        if c in ":.":
            r = t * 0.6
            cx = x + h * 0.08
            dots = [y + h * 0.3, y + h * 0.7] if c == ":" else [y + h - t]
            for cy in dots:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=on)
            x += h * 0.2
            continue
        lit = SEG.get(c, "")
        half = h / 2
        bars = {"a": (x + t, y, x + w - t, y + t), "g": (x + t, y + half - t / 2, x + w - t, y + half + t / 2),
                "d": (x + t, y + h - t, x + w - t, y + h), "f": (x, y + t, x + t, y + half - t / 2),
                "b": (x + w - t, y + t, x + w, y + half - t / 2), "e": (x, y + half + t / 2, x + t, y + h - t),
                "c": (x + w - t, y + half + t / 2, x + w, y + h - t)}
        for k, (x0, y0, x1, y1) in bars.items():
            if k in lit:
                d.rounded_rectangle([x0, y0, x1, y1], radius=t / 2, fill=on)
            elif off:
                d.rounded_rectangle([x0, y0, x1, y1], radius=t / 2, fill=off)
        if "|" in lit:
            d.rounded_rectangle([x + w / 2 - t / 2, y + h * 0.28, x + w / 2 + t / 2, y + h * 0.72], radius=t / 2, fill=on)
        x += w + h * 0.14


def fit_seg(text, h, maxw):
    while seg_width(text, h) > maxw and h > 40:
        h -= 6
    return h


def draw_whiteboard(img, d, box, sc):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=14, fill="#b9bcc0")
    d.rounded_rectangle([x0 + 16, y0 + 16, x1 - 16, y1 - 16], radius=6, fill="#fbfbf8")
    d.rectangle([x0 + 60, y1 - 4, x1 - 60, y1 + 14], fill="#9a9da1")
    rows = sc.get("rows") or []
    small, circ = set(sc.get("small") or []), sc.get("circle")
    tx, y = x0 + 64, y0 + 52
    if sc.get("title"):
        tf = ImageFont.truetype(MARKER, 92)
        d.text((tx, y), sc["title"], font=tf, fill="#1d4fb8")
        y += 140
    avail = y1 - 40 - y
    size = min(100, int(avail / max(1, len(rows)) / 1.3))
    for i, r in enumerate(rows):
        s = int(size * 0.38) if i in small else size
        f = ImageFont.truetype(MARKER, s)
        col = "#c62828" if i == circ else ("#1a1a1a" if i % 2 == 0 else "#1d4fb8")
        rh = int(size * 1.3)
        ty = y + (rh - s) // 2 if i in small else y
        d.text((tx, ty), r, font=f, fill=col)
        if i == circ:
            bb = d.textbbox((tx, ty), r, font=f)
            pad = 22
            for k in range(3):
                d.ellipse([bb[0] - pad - k * 3, bb[1] - pad + k * 2, bb[2] + pad + k * 2, bb[3] + pad - k * 2],
                          outline="#c62828", width=6)
        y += rh


def draw_clock(img, d, box, sc):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=22, fill="#141414")
    d.rounded_rectangle([x0 + 22, y0 + 22, x1 - 22, y1 - 22], radius=10, fill="#050505")
    text = sc.get("time", "0:00")
    label = sc.get("label")
    inner_w = x1 - x0 - 120
    h = fit_seg(text, int((y1 - y0) * (0.5 if label else 0.6)), inner_w)
    w = seg_width(text, h)
    ty = y0 + ((y1 - y0) - h) // 2 - (40 if label else 0)
    seg_text(d, x0 + (x1 - x0 - w) / 2, ty, text, h, "#ff2a1a", "#2a0b08")
    if label:
        f = F("Inter-Bold.otf", 44)
        lw = d.textlength(label, font=f)
        d.text((x0 + (x1 - x0 - lw) / 2, y1 - 120), label, font=f, fill="#ff6a55")


def draw_monitor(img, d, box, sc):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=40, fill="#2b2f33")
    d.rounded_rectangle([x0 + 40, y0 + 40, x1 - 40, y1 - 40], radius=16, fill="#a9b8a0")
    rows = (sc.get("rows") or [])[:3]
    label = sc.get("label")
    top = y0 + 70 + (60 if label else 0)
    if label:
        lf = F("Inter-Bold.otf", 36)
        d.text((x0 + 80, y0 + 66), label, font=lf, fill="#3c4a38")
    slot = (y1 - 70 - top) / max(1, len(rows))
    uf = F("Inter-Bold.otf", 40)
    for i, (val, unit) in enumerate(rows):
        h = fit_seg(val, int(slot * (0.72 if i == 0 else 0.6)), x1 - x0 - 380)
        yy = top + i * slot + (slot - h) / 2
        seg_text(d, x0 + 90, yy, val, h, "#1d2419", "#9aa891")
        d.text((x1 - 90 - d.textlength(unit, font=uf), yy + h - 46), unit, font=uf, fill="#1d2419")
        if i < len(rows) - 1:
            d.line([x0 + 70, top + (i + 1) * slot, x1 - 70, top + (i + 1) * slot], fill="#7f8f78", width=3)


SCENES = {"whiteboard": draw_whiteboard, "clock": draw_clock, "monitor": draw_monitor}


def render_scene(spec, out):
    sc = spec["scene"]
    if sc.get("type") not in SCENES:
        raise SystemExit("scene type must be one of: " + ", ".join(SCENES))
    lines = spec["lines"]
    if len(lines) > 2 or len(" ".join(lines).split()) > 14:
        raise SystemExit("Scene cards: 1 to 2 setup lines, 14 words max.")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    width = W - 2 * M
    for size in range(76, 47, -4):
        f = F("Inter-ExtraBold.otf", size)
        rows = [wrap(d, l, f, width) for l in lines]
        if sum(len(r) for r in rows) <= 3:
            break
    lh = int(size * 1.16)
    y = M - 10
    for r in rows:
        for row in r:
            d.text((M, y), row, font=f, fill=INK)
            y += lh
        y += int(size * 0.25)
    bottom = H - M - 70 - (90 if spec.get("tag") else 0)
    box = (M - 20, y + 30, W - M + 20, bottom)
    SCENES[sc["type"]](img, d, box, sc)
    if spec.get("tag"):
        ty = bottom + 40
        d.rectangle([M, ty + 6, M + 10, ty + 52], fill=ACCENT)
        d.text((M + 34, ty), spec["tag"], font=F("Inter-SemiBold.otf", 46), fill=GREY)
    d.text((M, H - M - 30), "@coach_chris_kenko", font=F("Inter-Medium.otf", 34), fill=GREY)
    img.save(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    import os
    os.makedirs(os.path.dirname(os.path.abspath(sys.argv[2])), exist_ok=True)
    render(json.load(open(sys.argv[1])), sys.argv[2])
