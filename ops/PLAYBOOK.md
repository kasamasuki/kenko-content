# Kenko daily Instagram playbook (@coach_chris_kenko)

Two feed posts per day, scheduled through Buffer the evening before (changed from one a day on 2026-10-17):
- 11:00am: coaching insight carousel (slot DATE-am).
- 4:00pm: relatable gym culture carousel, following the rotation below (slot DATE).
The two posts on the same day must cover different topics.
Updated 2026-10-15 after auditing 150 posts: relatable gym-culture carousels and Reels (Apr to Jul)
had a median reach of about 1,280; long educational posts with site links (Sep to Oct) had about 220.

## 11am slot: coaching insight, every day
- One sharp coach-level observation per carousel (form breakdowns, plateau causes, recovery mistakes, programming logic such as deloads, retests and energy systems). One idea per slide, no lecture.
- End the caption with "Save this for your next session." then a permitted CTA.
- Rotate themes across the week so no theme repeats within 7 days.

## 4pm slot: weekly rotation (by the weekday the post goes OUT)
- Mon: Relatable gym culture carousel ("that person in class", coach's-eye humour).
- Tue: Relatable gym culture carousel.
- Wed: Second-person story carousel ("You walk in at 5:05am. The whiteboard says..."). Never invent first-person events as if they happened to Chris.
- Thu: "Which slide is you?" carousel.
- Fri: Relatable gym culture carousel.
- Sat: "Which slide is you?" carousel (class types, workout moments, excuses). The format that reached 121K.
- Sun: Relatable gym culture carousel.
- Proof post: about 1 in 20 posts (roughly one every 10 days) replaces an 11am slot with a real product artifact, only when genuine data exists. Only proof posts may mention kenkoperformance.com (use --proof).

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
