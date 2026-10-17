#!/usr/bin/env python3
"""Schedule every queued post that is not in posted.log yet. Run by the schedule-post Action.

A queued post is queue/SLOT.json plus captions/SLOT.txt, where SLOT is YYYY-MM-DD (4pm post)
or YYYY-MM-DD-am (11am post):
  {"images": ["https://raw.githubusercontent.com/.../01.png", ...], "proof": false}
Past dates are skipped. Exits non-zero if any post fails, so the Action goes red."""
import datetime, glob, json, os, re, subprocess, sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
today = datetime.datetime.now(ZoneInfo("Australia/Melbourne")).date().isoformat()
logged = {l.split("\t")[0] for l in open(os.path.join(HERE, "posted.log")) if l.strip()}
failed = 0
for path in sorted(glob.glob(os.path.join(HERE, "queue", "*.json"))):
    slot = os.path.basename(path)[:-5]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(-am)?", slot) or slot in logged or slot[:10] < today:
        continue
    spec = json.load(open(path))
    images = spec["images"]
    if not all(isinstance(u, str) and u.startswith("https://raw.githubusercontent.com/kasamasuki/kenko-content/") for u in images):
        print(f"{slot}: image URLs must be raw.githubusercontent.com/kasamasuki/kenko-content URLs"); failed += 1; continue
    cmd = [sys.executable, os.path.join(HERE, "post_to_buffer.py"), slot, f"captions/{slot}.txt", *images]
    if spec.get("proof"):
        cmd.append("--proof")
    print(f"== {slot}: scheduling {len(images)} image(s)", flush=True)
    if subprocess.run(cmd, cwd=HERE).returncode:
        failed += 1
sys.exit(1 if failed else 0)
