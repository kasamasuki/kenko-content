# Kenko daily Instagram playbook (@coach_chris_kenko)

Core strategy (unchanged): two feed posts and one Story every day. Extra weekly posts (added 2026-10-24) sit on top and never replace a core slot. All scheduled through Buffer the evening before.
Core, every day:
- 11:00am: coaching insight Reel (slot DATE-am). Changed from a carousel on 2026-10-24 after the first Reel test worked.
- 4:00pm: relatable gym culture carousel, following the rotation below (slot DATE).
- 6:30pm: Story tied to the 4pm post (slot DATE-story).
Extras:
- Mon 5:30am: workout of the week Story (slot DATE-wod). Needs Chris's approval.
- Mon 7:30am: workout walkthrough Reel (slot DATE-early). Goes with the workout; needs the same approval.
- Tue, Thu, Sat 7:30am: movement of the week Reel (slot DATE-early).
- Wed 8:00pm: "Rate this workout" Story (slot DATE-rate).
All feed posts on the same day (11am Reel, 4pm carousel and any 7:30am Reel) must cover different topics.
Updated 2026-10-15 after auditing 150 posts: relatable gym-culture carousels and Reels (Apr to Jul)
had a median reach of about 1,280; long educational posts with site links (Sep to Oct) had about 220.

## 11am slot: coaching insight Reel, every day
- One sharp coach-level observation per Reel (form breakdowns, plateau causes, recovery mistakes, programming logic such as deloads, retests and energy systems). One idea per beat, no lecture.
- Format: faceless text Reel from tools/reel.py, 15 to 25 seconds. Write the spec like a carousel spec but tighter: a hook of 2 short lines, 4 to 5 beats, titles under ~35 characters, bodies under ~70 characters, end card with a CTA. Render to posts/DATE-am/reel.mp4 and queue {"video": URL}.
- The first second decides everything: the hook must be specific and land on the first frame.
- End the caption with "Save this for your next session." then a permitted CTA.
- Rotate themes across the week so no theme repeats within 7 days. Don't repeat the angle of that day's 7:30am Reel.

## Extra 7:30am Reels (slot DATE-early): Mon, Tue, Thu, Sat
- Same Reel format and length as the 11am slot (tools/reel.py, 15 to 25 seconds, hook of 2 short lines, 4 to 5 beats), rendered to posts/DATE-early/reel.mp4, caption ops/captions/DATE-early.txt ending "Save this for your next session." then a permitted CTA.
- Mon: "How to attack this week's workout". Breaks down that morning's workout of the week: the stimulus, a pacing target, the most common mistake, how to scale. Label "This week's workout". Hook names the workout, e.g. "21-15-9 wall balls and row. Here's the plan." Only posted if the workout is approved.
- Tue, Thu, Sat: Movement of the week. Pick one movement from Monday's workout (or a staple like the pull-up, wall ball, power clean, double-under) not used as movement of the week in the last 8 weeks. Tue: the setup. Thu: the most common mistake and its fix. Sat: the scaled version and when to use it. Label "Movement of the week". If there was no approved workout that week, pick a staple.

## Monday 5:30am: workout of the week Story
- One workout a week, Mondays only. Not daily: Chris's full programming stays in his product, so never post a week plan or a program, only this one session.
- Card from tools/workout.py, rendered to posts/DATE-wod/01.png and queued as ops/queue/DATE-wod.json ({"images": [URL]}) with NO caption file.
- Claude writes the workout. Rules:
  - Built for a general group class of mixed ability: a strength piece (15 to 20 minutes) and a metcon (8 to 20 minutes, always with a time cap).
  - Strength: submaximal sets only (for example 5 x 3 @ 75 to 82%, or build to a heavy 3 that still moves well). Never a 1RM test or anything to failure.
  - Metcon: common equipment only (barbell, dumbbells, kettlebells, rower, bike, pull-up bar, box, wall ball, skipping rope). Rx loads in kg as male/female (e.g. 43/30kg) plus one scaling line. No high-rep heavy Olympic lifts under fatigue, no high-skill gymnastics in large sets.
  - Alternate emphasis week to week (squat, hinge, press, pull, mixed) and the metcon format (for time, AMRAP, EMOM, intervals). Check the last 8 specs/*-wod.json so nothing repeats.
  - One "feel" line with the intended stimulus and a target time or score, one "Scale:" line, and "Reply with your time." (or "your score" / "your rounds").
- Chris approves every workout before it is scheduled. The Sunday evening run schedules the normal core slots for Monday as usual, renders and pushes the workout card and the 7:30am walkthrough Reel (caption kept in specs/DATE-early.txt until approved), but queues neither. It sends Chris the card for approval and arms a send_later check-in into its own session for 10:00pm Melbourne.
- When Chris approves (with any changes he asks for, re-rendering the card and Reel to match), move the caption to ops/captions/DATE-early.txt and queue ops/queue/DATE-wod.json and ops/queue/DATE-early.json together.
- If there is no approval by the 10:00pm check-in, or Chris rejects it: queue neither and tell him. The core Monday posts are unaffected. Never queue the workout without his explicit approval.

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

## Wednesday 8:00pm: "Rate this workout" Story (slot DATE-rate)
- Extra Story on top of the normal 6:30pm one. Card from tools/story.py to posts/DATE-rate/01.png, queued as ops/queue/DATE-rate.json ({"images": [URL]}), NO caption file.
- Show a deliberately absurd or famously awful workout (e.g. "100 burpees. Then 100 more. For time.") with kicker "Rate this workout" and options like "A. Love it", "B. Hate it", "C. Coach is unwell", then "Reply with A, B or C." Affectionate humour, never a workout anyone should actually attempt as written.

## Hooks (added 2026-10-24)
The hook is the first line of the caption AND the first slide or Reel frame. It decides whether anyone sees the rest.
- For every feed post, draft at least 5 candidate hooks, then pick the strongest. Specific beats general: a number, a named movement, a named moment ("5:05am", "round three", "the last rep").
- 10 words or fewer. Lands on the first frame. No warm-up words ("So,", "Here's the thing", "Let's talk about").
- Formats that work: "Stop [common habit]." / "You're not [X]. You're [Y]." / "[Common belief] is wrong." / "Coaches spot this in 3 seconds." / "The rep everyone cheats." / "We all know..." / a direct question.

### Provocative hooks: occasionally
- A provocative hook makes a bold, contrarian or slightly cheeky claim that makes people stop, disagree or tag someone. Use one about 2 to 3 times a week across all feed posts. Never two on the same day, never in the same slot two days running.
- It must be true, or a position an experienced coach would defend, and the post must pay it off by slide 2 or beat 2. No bait the content doesn't back up.
- Punch at habits, myths and gym culture, never at people: nothing mean about beginners, bodies, injuries, other gyms, coaches or named athletes. No health scare claims. Brand rules still apply (no "CrossFit", no emojis, no em dashes).
- Good examples: "Stretching won't fix your squat." / "You're not overtrained. You're under-slept." / "That PR didn't count. Check your depth." / "Stop using burpees as punishment." / "Your coach is lying about the last round." / "The 5am crowd isn't more disciplined. They just go to bed earlier."
- Too far (don't): anything that mocks a beginner or a body, "Your gym is ripping you off", fake stats, or claims like "Squats wreck your knees".

### Hook log
- Append one line per feed post to ops/hooks.log, in the same commit as its queue file: SLOT<TAB>standard|provocative<TAB>the hook. Read it before writing so provocative hooks stay occasional, and so no hook repeats.

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
