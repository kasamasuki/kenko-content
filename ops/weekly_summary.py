#!/usr/bin/env python3
"""Print a short summary of the last 7 days of posts from post_history.json (Markdown)."""
import datetime, json, os, sys
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "post_history.json")
posts = json.load(open(path))
now = datetime.datetime.now(datetime.timezone.utc)
week = []
for p in posts:
    sent = datetime.datetime.fromisoformat((p.get("sentAt") or p["dueAt"]).replace("Z", "+00:00"))
    if now - sent <= datetime.timedelta(days=7):
        m = {x["type"]: x["value"] for x in p.get("metrics") or []}
        hook = (p.get("text") or "").strip().splitlines()[0][:70] if p.get("text") else "(no caption)"
        week.append((sent, hook, m.get("reach", 0), m.get("shares", 0), m.get("saves", 0)))
print(f"# Weekly summary ({now.date().isoformat()})\n")
if not week:
    print("No posts sent in the last 7 days."); sys.exit()
week.sort()
tot = [sum(w[i] for w in week) for i in (2, 3, 4)]
best, worst = max(week, key=lambda w: w[2]), min(week, key=lambda w: w[2])
print(f"- Posts: {len(week)}. Reach {tot[0]} total, {tot[0] // len(week)} average. Shares {tot[1]}. Saves {tot[2]}.")
print(f"- Best: {best[0]:%a %d %b} \"{best[1]}\" (reach {best[2]}, shares {best[3]}, saves {best[4]})")
print(f"- Worst: {worst[0]:%a %d %b} \"{worst[1]}\" (reach {worst[2]}, shares {worst[3]}, saves {worst[4]})")
print("\n| Date | Hook | Reach | Shares | Saves |\n|---|---|---|---|---|")
for w in week:
    print(f"| {w[0]:%a %d %b} | {w[1]} | {w[2]} | {w[3]} | {w[4]} |")
