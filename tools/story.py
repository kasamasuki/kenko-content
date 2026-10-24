#!/usr/bin/env python3
"""Render a Kenko Instagram Story card (1080x1920 PNG) from a JSON spec.

Usage: python3 tools/story.py specs/DATE-story.json posts/DATE-story/01.png

Spec:
{
  "kicker": "Quick one",                         small green label
  "lines": ["Partner workout.", "Who carries", "who?"],   big text, last line green
  "options": ["A. I carry", "B. I get carried"],  optional, 2 to 4 answer rows
  "ask": "Reply with A or B."                     small grey line that invites a DM reply
}
Stories are auto-published by Buffer, which means no stickers, polls, links or captions
(those force manual publishing). So the card itself asks for a DM reply.
Text stays clear of the top 260px (profile bar) and bottom 380px (reply bar).
Brand: #0a0a0a, white, #00FF87, Inter. No emojis, hashtags or em dashes.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1080, 1920, 96
TOP, BOTTOM = 260, 1540
BG, GREEN, WHITE, GREY, BOX = "#0a0a0a", "#00FF87", "#ffffff", "#9a9a9a", "#1c1c1c"
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


def render(spec, out):
    for k in ("lines",):
        if not spec.get(k):
            raise SystemExit(f"Spec needs {k}.")
    opts = spec.get("options", [])
    if opts and not 2 <= len(opts) <= 4:
        raise SystemExit("Use 2 to 4 options.")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    width = W - 2 * M
    for size in range(124, 63, -4):
        f = F("Inter-ExtraBold.otf", size)
        rows = [(l, i) for i, line in enumerate(spec["lines"]) for l in wrap(d, line, f, width)]
        head_h = len(rows) * size * 1.15
        opt_h = len(opts) * 150 + (60 if opts else 0)
        total = 90 + head_h + opt_h + (110 if spec.get("ask") else 0)
        if total <= BOTTOM - TOP:
            break
    else:
        raise SystemExit("Story text too long; shorten it.")
    y = TOP + (BOTTOM - TOP - total) / 2
    d.rectangle([M, y, M + 56, y + 8], fill=GREEN)
    d.text((M, y + 30), spec.get("kicker", "").upper(), font=F("Inter-Bold.otf", 36), fill=GREEN)
    y += 90
    for text, i in rows:
        d.text((M, y), text, font=f, fill=GREEN if i == len(spec["lines"]) - 1 else WHITE)
        y += size * 1.15
    if opts:
        y += 60
        of = F("Inter-SemiBold.otf", 50)
        for o in opts:
            if d.textlength(o, font=of) > width - 80:
                raise SystemExit(f"Option too long: {o}")
            d.rounded_rectangle([M, y, W - M, y + 120], radius=24, fill=BOX)
            d.text((M + 40, y + 60), o, font=of, fill=WHITE, anchor="lm")
            y += 150
    if spec.get("ask"):
        d.text((M, y + 50), spec["ask"], font=F("Inter-Medium.otf", 44), fill=GREY)
    d.text((M, BOTTOM + 70), "@coach_chris_kenko", font=F("Inter-Medium.otf", 34), fill=GREEN)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out)
    print(out)


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
