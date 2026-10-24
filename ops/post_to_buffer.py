#!/usr/bin/env python3
"""Schedule one Instagram feed post (single image, carousel or Reel) on Buffer.
Usage: post_to_buffer.py SLOT captions/SLOT.txt IMAGE_URL [IMAGE_URL ...] [--proof] [--dry-run]
       post_to_buffer.py SLOT captions/SLOT.txt VIDEO_URL.mp4 [--dry-run]   (Reel, also shared to feed)
SLOT is YYYY-MM-DD for the 4pm post or YYYY-MM-DD-am for the 11am post (Melbourne time).
SLOT YYYY-MM-DD-story is the daily Story (6:30pm; 1 to 10 images or one .mp4; no caption, since a
Story caption forces Buffer into manual notification publishing).
SLOT YYYY-MM-DD-wod is the Monday workout-of-the-week Story (5:30am; same rules as -story). An extra one-off Reel uses YYYY-MM-DD-reel and needs --due=HH:MM (Melbourne); --due overrides any slot's time.
Pass slide URLs in order for a carousel (max 10). --proof allows a kenkoperformance.com mention.
Reads the API key from the BUFFER_KEY environment variable (a GitHub Actions secret),
falling back to buffer_key.txt next to this script. Logs to posted.log
and refuses to schedule the same slot twice."""
import json, sys, os, urllib.request, datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNEL_ID = "6a97e322065799be4671f725"   # @coach_chris_kenko
POST_TIMES = {"pm": (16, 0), "am": (11, 0), "story": (18, 30), "wod": (5, 30)}
MAX_WORDS = 80
THUMB_MS = 1500   # Reel cover frame: the hook is fully on screen by 1.5s

args = [a for a in sys.argv[1:] if not a.startswith("--")]
slot, caption_path, images = args[0], args[1], args[2:]
date = slot[:10]
if slot not in (date, date + "-am", date + "-reel", date + "-story", date + "-wod"):
    sys.exit("SLOT must be YYYY-MM-DD, YYYY-MM-DD-am, YYYY-MM-DD-story, YYYY-MM-DD-wod or YYYY-MM-DD-reel.")
is_story = slot.endswith(("-story", "-wod"))
due_arg = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--due=")), None)
if slot.endswith("-reel") and not due_arg:
    sys.exit("A -reel slot needs --due=HH:MM (Melbourne time).")
post_hour, post_min = (map(int, due_arg.split(":")) if due_arg
                       else POST_TIMES["wod" if slot.endswith("-wod") else "story" if is_story else "am" if slot.endswith("-am") else "pm"])
dry, proof = "--dry-run" in sys.argv, "--proof" in sys.argv
is_reel = any(u.lower().endswith(".mp4") for u in images)
if is_reel and len(images) != 1:
    sys.exit("A Reel or video Story takes exactly one .mp4 URL and no images.")
if not 1 <= len(images) <= 10:
    sys.exit("Give 1 to 10 image URLs.")

log_path = os.path.join(HERE, "posted.log")
if os.path.exists(log_path) and any(l.startswith(slot + "\t") for l in open(log_path)):
    sys.exit(f"Already scheduled for {slot}; not posting twice.")

cap_file = caption_path if os.path.exists(caption_path) else os.path.join(HERE, caption_path)
if is_story:
    if os.path.exists(cap_file) and open(cap_file).read().strip():
        sys.exit("Stories go out with no caption (a caption forces manual publishing). Put the text on the card.")
    caption = ""
else:
    caption = open(cap_file).read().strip()
for bad, why in [("—", "em dash"), ("#", "hashtag"), ("crossfit", "the word CrossFit")]:
    if bad in caption.lower():
        sys.exit(f"Caption breaks brand rules: contains {why}.")
if not proof and ("kenkoperformance" in caption.lower() or "link in bio" in caption.lower()):
    sys.exit("Caption links to the site; only proof posts (--proof) may do that.")
if len(caption.split()) > MAX_WORDS:
    sys.exit(f"Caption is {len(caption.split())} words; keep it under {MAX_WORDS}.")
if caption and len(caption.splitlines()[0].split()) > 10:
    sys.exit("Hook (first line) is over 10 words.")
if any(ord(c) > 0x2600 for c in caption):
    sys.exit("Caption breaks brand rules: contains an emoji or symbol.")

local = datetime.datetime.fromisoformat(date).replace(hour=post_hour, minute=post_min, tzinfo=ZoneInfo("Australia/Melbourne"))
if local < datetime.datetime.now(datetime.timezone.utc):
    sys.exit(f"Due time {local:%Y-%m-%d %H:%M} Melbourne is already past.")
due = local.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

query = """mutation($input: CreatePostInput!) { createPost(input: $input) {
  ... on PostActionSuccess { post { id dueAt } }
  ... on MutationError { message } } }"""
variables = {"input": {
    "text": caption, "channelId": CHANNEL_ID, "schedulingType": "automatic",
    "mode": "customScheduled", "dueAt": due,
    "assets": ([{"video": {"url": images[0], "metadata": {"thumbnailOffset": THUMB_MS}}}] if is_reel
               else [{"image": {"url": u}} for u in images]),
    "metadata": {"instagram": {"type": "story" if is_story else "reel" if is_reel else "post",
                               "shouldShareToFeed": not is_story}},
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
        f.write(f"{slot}\t{post['post']['id']}\t{due}\t{images[0]}\t{'story' if is_story else 'reel' if is_reel else f'{len(images)} images'}\n")
else:
    sys.exit(1)
