#!/usr/bin/env python3
"""Schedule one Instagram feed post (single image, carousel or Reel) on Buffer.
Usage: post_to_buffer.py SLOT captions/SLOT.txt IMAGE_URL [IMAGE_URL ...] [--proof] [--dry-run]
       post_to_buffer.py SLOT captions/SLOT.txt VIDEO_URL.mp4 [--dry-run]   (Reel, also shared to feed)
SLOT is YYYY-MM-DD for the 4pm post or YYYY-MM-DD-am for the 11am post (Melbourne time).
Pass slide URLs in order for a carousel (max 10). --proof allows a kenkoperformance.com mention.
Reads the API key from the BUFFER_KEY environment variable (a GitHub Actions secret),
falling back to buffer_key.txt next to this script. Logs to posted.log
and refuses to schedule the same slot twice."""
import json, sys, os, urllib.request, datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNEL_ID = "6a97e322065799be4671f725"   # @coach_chris_kenko
POST_HOURS = {"pm": 16, "am": 11}
MAX_WORDS = 80
THUMB_MS = 1500   # Reel cover frame: the hook is fully on screen by 1.5s

args = [a for a in sys.argv[1:] if not a.startswith("--")]
slot, caption_path, images = args[0], args[1], args[2:]
date = slot[:10]
post_hour = POST_HOURS["am" if slot.endswith("-am") else "pm"]
if slot not in (date, date + "-am"):
    sys.exit("SLOT must be YYYY-MM-DD or YYYY-MM-DD-am.")
dry, proof = "--dry-run" in sys.argv, "--proof" in sys.argv
is_reel = any(u.lower().endswith(".mp4") for u in images)
if is_reel and len(images) != 1:
    sys.exit("A Reel takes exactly one .mp4 URL and no images.")
if not 1 <= len(images) <= 10:
    sys.exit("Give 1 to 10 image URLs.")

log_path = os.path.join(HERE, "posted.log")
if os.path.exists(log_path) and any(l.startswith(slot + "\t") for l in open(log_path)):
    sys.exit(f"Already scheduled for {slot}; not posting twice.")

caption = open(caption_path if os.path.exists(caption_path) else os.path.join(HERE, caption_path)).read().strip()
for bad, why in [("—", "em dash"), ("#", "hashtag"), ("crossfit", "the word CrossFit")]:
    if bad in caption.lower():
        sys.exit(f"Caption breaks brand rules: contains {why}.")
if not proof and ("kenkoperformance" in caption.lower() or "link in bio" in caption.lower()):
    sys.exit("Caption links to the site; only proof posts (--proof) may do that.")
if len(caption.split()) > MAX_WORDS:
    sys.exit(f"Caption is {len(caption.split())} words; keep it under {MAX_WORDS}.")
if len(caption.splitlines()[0].split()) > 10:
    sys.exit("Hook (first line) is over 10 words.")
if any(ord(c) > 0x2600 for c in caption):
    sys.exit("Caption breaks brand rules: contains an emoji or symbol.")

local = datetime.datetime.fromisoformat(date).replace(hour=post_hour, tzinfo=ZoneInfo("Australia/Melbourne"))
due = local.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

query = """mutation($input: CreatePostInput!) { createPost(input: $input) {
  ... on PostActionSuccess { post { id dueAt } }
  ... on MutationError { message } } }"""
variables = {"input": {
    "text": caption, "channelId": CHANNEL_ID, "schedulingType": "automatic",
    "mode": "customScheduled", "dueAt": due,
    "assets": ([{"video": {"url": images[0], "metadata": {"thumbnailOffset": THUMB_MS}}}] if is_reel
               else [{"image": {"url": u}} for u in images]),
    "metadata": {"instagram": {"type": "reel" if is_reel else "post", "shouldShareToFeed": True}},
}}
if dry:
    print(json.dumps(variables, indent=2)); sys.exit()

key = os.environ.get("BUFFER_KEY") or open(os.path.join(HERE, "buffer_key.txt")).read().strip()
req = urllib.request.Request("https://api.buffer.com", method="POST",
    data=json.dumps({"query": query, "variables": variables}).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
resp = json.load(urllib.request.urlopen(req, timeout=30))
print(json.dumps(resp, indent=2))
post = (resp.get("data") or {}).get("createPost") or {}
if "post" in post:
    with open(log_path, "a") as f:
        f.write(f"{slot}\t{post['post']['id']}\t{due}\t{images[0]}\t{'reel' if is_reel else f'{len(images)} images'}\n")
else:
    sys.exit(1)
