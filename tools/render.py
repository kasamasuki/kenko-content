#!/usr/bin/env python3
"""Render a Kenko feed post (1080x1350) from a JSON spec.

Usage: python3 tools/render.py spec.json out.png

Spec fields:
  label      small grey kicker, e.g. "COACH'S NOTES  /  SQUAT"
  headline   list of 1-3 short lines; the LAST line is drawn in green
  items      list of [main line, sub line] pairs, 2-5 of them (sub line may be "")
  footer     bottom-left line, default "Save this for your next session."
Brand: #0a0a0a background, white text, #00FF87 accents, Inter. No emojis.
"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG, GREEN, WHITE, GREY, RULE = "#0a0a0a", "#00FF87", "#ffffff", "#8a8a8a", "#222222"
FONT_DIR = "/usr/share/fonts/opentype/inter/"
M = 96  # side margin


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(spec, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([M, M, M + 56, M + 8], fill=GREEN)
    d.text((M, M + 40), spec.get("label", "").upper(), font=font("Inter-SemiBold.otf", 28), fill=GREY)

    # Headline: shrink until it fits on one line per entry.
    heads = spec["headline"]
    size = 76
    while size > 48 and any(d.textlength(h, font=font("Inter-ExtraBold.otf", size)) > W - 2 * M for h in heads):
        size -= 4
    hf = font("Inter-ExtraBold.otf", size)
    y = M + 110
    for i, line in enumerate(heads):
        d.text((M, y), line, font=hf, fill=GREEN if i == len(heads) - 1 else WHITE)
        y += int(size * 1.26)
    y += 50

    items = spec["items"]
    main_f, sub_f, num_f = font("Inter-SemiBold.otf", 40), font("Inter-Regular.otf", 32), font("Inter-Bold.otf", 40)
    text_w = W - 2 * M - 90
    blocks = []
    for main, sub in items:
        ml, sl = wrap(d, main, main_f, text_w), wrap(d, sub, sub_f, text_w) if sub else []
        blocks.append((ml, sl, len(ml) * 54 + len(sl) * 44))
    avail = H - 190 - y
    gap = max(30, min(70, (avail - sum(b[2] for b in blocks)) // max(1, len(blocks))))
    for n, (ml, sl, _) in enumerate(blocks, 1):
        d.text((M, y), f"{n:02d}", font=num_f, fill=GREEN)
        for line in ml:
            d.text((M + 90, y - 2), line, font=main_f, fill=WHITE)
            y += 54
        for line in sl:
            d.text((M + 90, y), line, font=sub_f, fill=GREY)
            y += 44
        y += gap
    if y > H - 170:
        sys.exit(f"Content overflows the card by {y - (H - 170)}px; shorten the items.")

    d.line([M, H - 150, W - M, H - 150], fill=RULE, width=2)
    d.text((M, H - 118), spec.get("footer", "Save this for your next session."), font=font("Inter-Medium.otf", 30), fill=WHITE)
    d.text((W - M, H - 118), "@coach_chris_kenko", font=font("Inter-Medium.otf", 30), fill=GREEN, anchor="ra")
    img.save(out)


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
