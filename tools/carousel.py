#!/usr/bin/env python3
"""Render a Kenko carousel (1080x1350 slides) from a JSON spec.

Usage: python3 tools/carousel.py specs/DATE.json posts/DATE
Writes posts/DATE/01.png, 02.png, ... and prints the file list.

Spec:
{
  "label": "GYM CULTURE",                      kicker on the cover
  "cover": ["We all know", "that person", "in class."],   last line green
  "slides": [                                   3 to 8 content slides
     {"title": "The warm-up skipper.", "body": "Says they're warm. Their hips say otherwise.", "tag": "Slide 1"},
     ...
  ],
  "end": ["Tag the training partner", "who is slide 4."]   last line green
}
Each slide: "title" (required, big), "body" (optional, grey), "tag" (optional small green kicker,
e.g. "IS THIS YOU?"). Keep titles under ~40 characters and bodies under ~120.
Brand: #0a0a0a, white, #00FF87, Inter. No emojis, hashtags or em dashes.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1080, 1350, 96
BG, GREEN, WHITE, GREY, DIM, RULE = "#0a0a0a", "#00FF87", "#ffffff", "#8f8f8f", "#4a4a4a", "#222222"
FD = "/usr/share/fonts/opentype/inter/"
HANDLE = "@coach_chris_kenko"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def wrap(d, text, fnt, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def fit_lines(d, lines, name, start, min_size, width, max_h, lh=1.18):
    """Largest size where every given line wraps to fit within max_h."""
    size = start
    while size >= min_size:
        f = F(name, size)
        wrapped = [wrap(d, l, f, width) for l in lines]
        h = sum(len(w) for w in wrapped) * size * lh
        if h <= max_h and all(d.textlength(x, font=f) <= width for w in wrapped for x in w):
            return f, size, wrapped
        size -= 4
    raise SystemExit(f"Text too long to fit: {lines}")


def base(n, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((M, H - 118), HANDLE, font=F("Inter-Medium.otf", 30), fill=GREEN)
    d.text((W - M, H - 118), f"{n:02d} / {total:02d}", font=F("Inter-Medium.otf", 30), fill=DIM, anchor="ra")
    d.line([M, H - 150, W - M, H - 150], fill=RULE, width=2)
    return img, d


def cover(spec, total):
    img, d = base(1, total)
    d.rectangle([M, M, M + 56, M + 8], fill=GREEN)
    d.text((M, M + 40), spec.get("label", "").upper(), font=F("Inter-SemiBold.otf", 28), fill=GREY)
    f, size, wrapped = fit_lines(d, spec["cover"], "Inter-ExtraBold.otf", 112, 64, W - 2 * M, H - 560)
    flat = [(x, i) for i, w in enumerate(wrapped) for x in w]
    y = (H - 150 - len(flat) * size * 1.18) / 2 + 20
    for text, i in flat:
        d.text((M, y), text, font=f, fill=GREEN if i == len(wrapped) - 1 else WHITE)
        y += size * 1.18
    d.text((W - M, H - 220), "Swipe  →", font=F("Inter-SemiBold.otf", 34), fill=GREEN, anchor="ra")
    return img


def content(sl, n, total):
    img, d = base(n, total)
    y = M + 10
    if sl.get("tag"):
        d.text((M, y), sl["tag"].upper(), font=F("Inter-Bold.otf", 30), fill=GREEN)
        y += 70
    tf, ts, tw = fit_lines(d, [sl["title"]], "Inter-ExtraBold.otf", 92, 56, W - 2 * M, 520)
    body_h = 0
    if sl.get("body"):
        bf = F("Inter-Regular.otf", 44)
        bw = wrap(d, sl["body"], bf, W - 2 * M)
        body_h = len(bw) * 60 + 50
    block = len(tw[0]) * ts * 1.18 + body_h
    # Fixed anchor so titles sit at the same height on every slide while swiping.
    y = max(y, 400 if block < 600 else (H - 150 - block) / 2)
    for line in tw[0]:
        d.text((M, y), line, font=tf, fill=WHITE)
        y += ts * 1.18
    if sl.get("body"):
        y += 50
        d.rectangle([M, y - 26, M + 40, y - 20], fill=GREEN)
        for line in bw:
            d.text((M, y), line, font=bf, fill=GREY)
            y += 60
    if y > H - 170:
        raise SystemExit(f"Slide {n} overflows; shorten it.")
    return img


def end(spec, total):
    img, d = base(total, total)
    f, size, wrapped = fit_lines(d, spec["end"], "Inter-ExtraBold.otf", 88, 56, W - 2 * M, H - 600)
    flat = [(x, i) for i, w in enumerate(wrapped) for x in w]
    y = (H - 150 - len(flat) * size * 1.18) / 2
    for text, i in flat:
        d.text((M, y), text, font=f, fill=GREEN if i == len(wrapped) - 1 else WHITE)
        y += size * 1.18
    d.text((M, y + 50), "Follow for more.", font=F("Inter-Medium.otf", 36), fill=GREY)
    return img


def render(spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    slides = spec["slides"]
    if not 3 <= len(slides) <= 8:
        raise SystemExit("Use 3 to 8 content slides.")
    total = len(slides) + 2
    imgs = [cover(spec, total)] + [content(s, i + 2, total) for i, s in enumerate(slides)] + [end(spec, total)]
    paths = []
    for i, im in enumerate(imgs, 1):
        p = os.path.join(outdir, f"{i:02d}.png")
        im.save(p)
        paths.append(p)
    print("\n".join(paths))


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
