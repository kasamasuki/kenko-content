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
Brand: no emojis, hashtags or em dashes, no people, no logos.
"""
import json, re, sys
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
    text = " ".join(lines + [spec.get("tag", "")])
    if len(text.split()) > 25:
        raise SystemExit("Too long for a meme card: 25 words max.")
    if "#" in text or "—" in text or re.search("[\U0001F300-\U0001FAFF☀-➿]", text):
        raise SystemExit("No hashtags, emojis or em dashes.")


def render(spec, out):
    check(spec)
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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    import os
    os.makedirs(os.path.dirname(os.path.abspath(sys.argv[2])), exist_ok=True)
    render(json.load(open(sys.argv[1])), sys.argv[2])
