# Kenko daily Instagram playbook (@coach_chris_kenko)

One feed post per day at 4:00pm Melbourne time, scheduled through Buffer the evening before.
Updated 2026-10-15 after auditing 150 posts: relatable gym-culture carousels and Reels (Apr to Jul)
had a median reach of about 1,280; long educational posts with site links (Sep to Oct) had about 220.

## Weekly rotation (by the weekday the post goes OUT)
- Mon: Relatable gym culture carousel ("that person in class", coach's-eye humour).
- Tue: Coaching insight carousel. One sharp observation, one idea per slide, no lecture.
- Wed: Second-person story carousel ("You walk in at 5:05am. The whiteboard says..."). Never invent first-person events as if they happened to Chris.
- Thu: Coaching insight carousel.
- Fri: Relatable gym culture carousel.
- Sat: "Which slide is you?" carousel (class types, workout moments, excuses). The format that reached 121K.
- Sun: Relatable gym culture carousel.
- Proof post: about 1 in 20 posts replaces a slot with a real product artifact, only when genuine data exists. Only proof posts may mention kenkoperformance.com (use --proof).

## What works (from the audit)
- Carousels of 5 to 8 slides beat single images. Default to carousels (tools/carousel.py).
- Short, punchy hooks of 10 words or fewer. Questions and "we all know..." framings did best.
- Short captions: under 60 words is the target, 80 is the hard limit. The slides carry the content.
- Shares drive reach. Write things people send to a training partner. End with a tag CTA.
- No links in captions outside proof posts. Link posts underperformed.

## Hard brand rules (never break)
- No emojis anywhere. No hashtags. No em dashes (use a period or comma).
- Never use the word "CrossFit".
- Faceless: no people, no faces. Text-on-dark graphics only.
- CTAs: "Follow for more" / "Tag a friend" / "Tag a training partner". Never "Download".
- No motivational, mindset, "new week energy" or inspirational quote posts.
- Humour is affectionate, never mean about beginners, bodies or injuries.
- Premium, confident, no-fluff tone. Coach talking to athletes.

## Look
- 1080x1350 slides, #0a0a0a background, white text, #00FF87 accent, Inter.
- Carousels: tools/carousel.py in this repo (kasamasuki/kenko-content). Single cards: tools/render.py.

## Files (all under ops/ in kasamasuki/kenko-content; this repo is public, so nothing secret goes here)
- captions/YYYY-MM-DD.txt  caption for each post (read these to avoid repeating topics)
- queue/YYYY-MM-DD.json    slide URLs for a post; pushing it runs the schedule-post Action
- posted.log               date, Buffer post id, due time, first image URL, image count
- weekly-summary.md        last week's reach, shares, saves, best and worst post (fetch-history Action, Mondays)
- BUFFER_KEY secret        Buffer API key, stored as a GitHub Actions secret (never print or commit it). Expires 2027-10-15.
- post_to_buffer.py        schedules the post; refuses duplicates and rule-breaking captions
