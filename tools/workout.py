#!/usr/bin/env python3
"""Render the Kenko workout-of-the-week Story card (1080x1920 PNG) from a JSON spec.

Usage: python3 tools/workout.py specs/DATE-wod.json posts/DATE-wod/01.png

Spec:
{
  "kicker": "Workout of the week",                 small green label
  "title": "Squat and sprint.",                    big white headline, short
  "parts": [                                       1 or 2 blocks, usually strength then metcon
    {"name": "Strength", "detail": "Back squat",
     "lines": ["5 x 3 @ 78 to 82%", "Rest 2 to 3 min"]},
    {"name": "Metcon", "detail": "For time, 12 min cap",
     "lines": ["21-15-9", "Wall balls 9/6kg", "Calorie row"]}
  ],
  "feel": "Fast and ugly. Under 8 minutes.",       one line: the stimulus
  "scale": "Scale: 15-12-9, lighter ball.",         one line: the scaling option
  "ask": "Reply with your time."                   small grey line that invites a DM reply
}
Same safe zone as tools/story.py: clear of the top 260px and bottom 380px.
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


def check(text):
    for bad, why in [("—", "em dash"), ("#", "hashtag"), ("crossfit", "the word CrossFit")]:
        if bad in text.lower():
            raise SystemExit(f"Brand rule: {why} in {text!r}")
    if any(ord(c) > 0x2600 for c in text):
        raise SystemExit(f"Brand rule: emoji or symbol in {text!r}")


def render(spec, out):
    parts = spec.get("parts", [])
    if not spec.get("title") or not 1 <= len(parts) <= 2:
        raise SystemExit("Spec needs a title and 1 or 2 parts.")
    texts = [spec["title"], spec.get("kicker", ""), spec.get("feel", ""), spec.get("scale", ""), spec.get("ask", "")]
    for p in parts:
        texts += [p["name"], p.get("detail", ""), *p["lines"]]
    for t in texts:
        check(t)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    inner = W - 2 * M - 80
    # shrink everything together until it fits the safe zone
    for scale in [x / 100 for x in range(100, 59, -4)]:
        tf, nf, df = F("Inter-ExtraBold.otf", int(96 * scale)), F("Inter-Bold.otf", int(34 * scale)), F("Inter-Medium.otf", int(40 * scale))
        lf, sf = F("Inter-SemiBold.otf", int(54 * scale)), F("Inter-Medium.otf", int(42 * scale))
        too_wide = d.textlength(spec["title"], font=tf) > W - 2 * M or any(
            d.textlength(l, font=lf) > inner or d.textlength(p.get("detail", ""), font=df) > inner
            for p in parts for l in p["lines"])
        too_wide |= any(d.textlength(spec.get(k, ""), font=sf) > W - 2 * M for k in ("feel", "scale", "ask"))
        part_h = [40 + nf.size * 1.3 + (df.size * 1.4 if p.get("detail") else 0) + len(p["lines"]) * lf.size * 1.35 + 30
                  for p in parts]
        extras = sum(sf.size * 1.5 for k in ("feel", "scale") if spec.get(k)) + (sf.size * 2 if spec.get("ask") else 0)
        total = 90 + tf.size * 1.2 + 40 + sum(part_h) + 30 * (len(parts) - 1) + 30 + extras
        if not too_wide and total <= BOTTOM - TOP:
            break
    else:
        raise SystemExit("Workout card too long or too wide; shorten it.")
    y = TOP + (BOTTOM - TOP - total) / 2
    d.rectangle([M, y, M + 56, y + 8], fill=GREEN)
    d.text((M, y + 30), spec.get("kicker", "Workout of the week").upper(), font=F("Inter-Bold.otf", 36), fill=GREEN)
    y += 90
    d.text((M, y), spec["title"], font=tf, fill=WHITE)
    y += tf.size * 1.2 + 40
    for p, ph in zip(parts, part_h):
        d.rounded_rectangle([M, y, W - M, y + ph], radius=24, fill=BOX)
        yy = y + 40
        d.text((M + 40, yy), p["name"].upper(), font=nf, fill=GREEN)
        yy += nf.size * 1.3
        if p.get("detail"):
            d.text((M + 40, yy), p["detail"], font=df, fill=GREY)
            yy += df.size * 1.4
        for l in p["lines"]:
            d.text((M + 40, yy), l, font=lf, fill=WHITE)
            yy += lf.size * 1.35
        y += ph + 30
    y += 30
    for k, col in (("feel", WHITE), ("scale", GREY)):
        if spec.get(k):
            d.text((M, y), spec[k], font=sf, fill=col)
            y += sf.size * 1.5
    if spec.get("ask"):
        d.text((M, y + sf.size * 0.5), spec["ask"], font=sf, fill=GREEN)
    d.text((M, BOTTOM + 70), "@coach_chris_kenko", font=F("Inter-Medium.otf", 34), fill=GREEN)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out)
    print(out)


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
