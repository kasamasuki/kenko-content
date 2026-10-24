# Kenko daily Instagram playbook (@coach_chris_kenko)

Two feed posts and one Story per day (plus a Monday workout Story), scheduled through Buffer the evening before:
- Monday 5:30am: workout of the week Story (slot DATE-wod), added 2026-10-24. Mondays only.
- 11:00am: coaching insight Reel (slot DATE-am). Changed from a carousel on 2026-10-24 after the first Reel test worked.
- 4:00pm: relatable gym culture carousel, following the rotation below (slot DATE).
- 6:30pm: Story (slot DATE-story), added 2026-10-24.
The two feed posts on the same day must cover different topics.
Updated 2026-10-15 after auditing 150 posts: relatable gym-culture carousels and Reels (Apr to Jul)
had a median reach of about 1,280; long educational posts with site links (Sep to Oct) had about 220.

## 11am slot: coaching insight Reel, every day
- One sharp coach-level observation per Reel (form breakdowns, plateau causes, recovery mistakes, programming logic such as deloads, retests and energy systems). One idea per beat, no lecture.
- Format: faceless text Reel from tools/reel.py, 15 to 25 seconds. Write the spec like a carousel spec but tighter: a hook of 2 short lines, 4 to 5 beats, titles under ~35 characters, bodies under ~70 characters, end card with a CTA. Render to posts/DATE-am/reel.mp4 and queue {"video": URL}.
- The first second decides everything: the hook must be specific and land on the first frame.
- End the caption with "Save this for your next session." then a permitted CTA.
- Rotate themes across the week so no theme repeats within 7 days. The weekly series below are the exception.

### Weekly 11am series (added 2026-10-24)
- Mon: "How to attack this week's workout". The Reel breaks down that morning's workout of the week: the stimulus, a pacing target, the most common mistake, how to scale. Label "This week's workout". Hook names the workout, e.g. "21-15-9 wall balls and row. Here's the plan."
- Tue, Thu, Sat: Movement of the week. Pick one movement from Monday's workout (or a staple like the pull-up, wall ball, power clean, double-under) not used as movement of the week in the last 8 weeks. Tue: the setup. Thu: the most common mistake and its fix. Sat: the scaled version and when to use it. Label "Movement of the week".
- Wed, Fri, Sun: normal rotating coaching insights (plateau causes, recovery mistakes, programming logic, energy systems).

## Monday 5:30am: workout of the week Story
- One workout a week, Mondays only. Not daily: Chris's full programming stays in his product, so never post a week plan or a program, only this one session.
- Card from tools/workout.py, rendered to posts/DATE-wod/01.png and queued as ops/queue/DATE-wod.json ({"images": [URL]}) with NO caption file.
- Claude writes the workout. Rules:
  - Built for a general group class of mixed ability: a strength piece (15 to 20 minutes) and a metcon (8 to 20 minutes, always with a time cap).
  - Strength: submaximal sets only (for example 5 x 3 @ 75 to 82%, or build to a heavy 3 that still moves well). Never a 1RM test or anything to failure.
  - Metcon: common equipment only (barbell, dumbbells, kettlebells, rower, bike, pull-up bar, box, wall ball, skipping rope). Rx loads in kg as male/female (e.g. 43/30kg) plus one scaling line. No high-rep heavy Olympic lifts under fatigue, no high-skill gymnastics in large sets.
  - Alternate emphasis week to week (squat, hinge, press, pull, mixed) and the metcon format (for time, AMRAP, EMOM, intervals). Check the last 8 specs/*-wod.json so nothing repeats.
  - One "feel" line with the intended stimulus and a target time or score, one "Scale:" line, and "Reply with your time." (or "your score" / "your rounds").
- Chris approves every workout before it is scheduled. The Sunday evening run renders and pushes the card but does NOT queue ops/queue/DATE-wod.json. It sends Chris the card for approval, and the workout is queued only after he replies in that run's session approving it (with any changes he asks for). No approval by 5:00am Monday means no workout Story that week. Never queue it without his explicit approval.
- That Monday's 11am Reel breaks this workout down. If the workout is changed at approval, re-render the Reel to match before it goes out. If the workout is not approved, the 11am Reel is still scheduled (it only describes the workout), so keep it general enough to stand alone, or swap it for a normal coaching insight if Chris rejects the workout. The Monday 4pm carousel and 6:30pm Story stay on the normal rotation.

## 4pm slot: weekly rotation (by the weekday the post goes OUT)
- Mon: Relatable gym culture carousel ("that person in class", coach's-eye humour).
- Tue: Relatable gym culture carousel.
- Wed: Second-person story carousel ("You walk in at 5:05am. The whiteboard says..."). Never invent first-person events as if they happened to Chris.
- Thu: "Which slide is you?" carousel.
- Fri: Relatable gym culture carousel.
- Sat: "Which slide is you?" carousel (class types, workout moments, excuses). The format that reached 121K.
- Sun: Relatable gym culture carousel.
- Proof post: about 1 in 20 posts (roughly one every 10 days) replaces an 11am slot with a real product artifact, only when genuine data exists. Only proof posts may mention kenkoperformance.com (use --proof).

## 6:30pm Story, every day
- One 1080x1920 card from tools/story.py, queued as ops/queue/DATE-story.json ({"images": [URL]}) with NO caption file.
- Buffer auto-publishes Stories only without stickers, polls, links, music or captions, so the card itself asks for a DM reply: a quick question tied to that day's 4pm post with 2 to 4 lettered options and "Reply with A, B or C." DM replies are the engagement signal we want.
- Same brand rules. Keep it light and quick to answer. No motivational quotes.
- Wednesday exception: "Rate this workout". Instead of tying to the 4pm post, show a deliberately absurd or famously awful workout (e.g. "100 burpees. Then 100 more. For time.") with kicker "Rate this workout" and options like "A. Love it", "B. Hate it", "C. Coach is unwell". Affectionate humour, never a workout anyone should actually attempt as written.

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
- Carousels: tools/carousel.py. Reels: tools/reel.py (1080x1920 MP4). Stories: tools/story.py (1080x1920 PNG). Workout card: tools/workout.py (1080x1920 PNG). Single cards: tools/render.py.

## Files (all under ops/ in kasamasuki/kenko-content; this repo is public, so nothing secret goes here)
- captions/YYYY-MM-DD.txt  caption for each post (read these to avoid repeating topics)
- queue/SLOT.json          slide URLs ({"images": [...]}) or a Reel ({"video": URL}); pushing it runs the schedule-post Action
- posted.log               date, Buffer post id, due time, first image URL, image count
- weekly-summary.md        last week's reach, shares, saves, best and worst post (fetch-history Action, Mondays)
- BUFFER_KEY secret        Buffer API key, stored as a GitHub Actions secret (never print or commit it). Expires 2027-10-15.
- post_to_buffer.py        schedules the post; refuses duplicates and rule-breaking captions
