# Kenko daily Instagram playbook (@coach_chris_kenko)

## Manager mandate (from 2026-11-02)
Chris has handed the account to Claude as social media manager. The goal is reach (and the shares that drive it).
- Claude decides content, slots, posting times, volume, formats, rotation, hook mix and the look, and edits this playbook itself. The weekly review (Mondays) is where changes are made, each one backed by numbers and logged in the Change log below.
- Fixed, never changed by Claude: no emojis, hashtags or em dashes; CTAs never "Download"; no motivational or quote posts; humour never mean about beginners, bodies or injuries; no health scare claims or fake stats; never post photos or video of real people (Claude has none) or anything imitating another account; never invent first-person events as Chris's; only proof posts mention kenkoperformance.com; one workout a week, never a program.
- Changeable on evidence: "faceless, text-on-dark only", colours and layout, the 4pm rotation, slot times and how many posts a day.
- The word "CrossFit" is allowed on Instagram from 2026-11-05 (Chris: the CrossFit branding ban applies only inside the Kenko app). Use it where it is how the audience describes itself ("the 6am CrossFit class", "CrossFit coaches"). Never imply Kenko is affiliated with or endorsed by CrossFit, and never use CrossFit logos.
- Chris's own posts (anything in Buffer's history without an ops/queue file, e.g. 30 Oct "gym buddy eye contact", 27 Oct "Coach: have you been doing your mobility?") are the benchmark: in the week to 1 Nov two of them earned 85 of 111 shares. Study what they do and borrow it.
- From 2026-11-06 Chris posts one meme Reel a day himself at about 9:30am (film or TV clip with a relatable class caption). His 3 Nov meme ("only guy at the 9:30 CrossFit class with all the mums that out-lift you") did 15.3k views and 1.7k interactions, more than every other post in the 30 days to 5 Nov combined. Claude's posts support his memes and must not compete with them: nothing Claude queues goes out between 8:30am and 11:30am except the Monday walkthrough Reel and the Tue/Thu/Sat 7:30am test Reels.
- The audience includes about 38k bought followers (Chris, 2026-11-05). Follower count and follower reach mean little. Judge everything on non-follower reach, shares, saves and profile visits/link taps.
- Reporting: Chris hears from Claude in the Monday report (results, changes made, ideas for him to film or post himself) and when something breaks. Daily runs are otherwise silent.
- The workout of the week no longer needs approval (Chris, 2026-11-02). It is queued with the core posts.

## Change log
- 2026-11-05 (agreed with Chris): Chris now posts a daily meme Reel at about 9:30am. 4pm relatable carousel paused (slot DATE): Chris's memes do relatable humour far better (15.3k vs about 700 views for carousels in the 30 days to 5 Nov). Coaching carousel moved from 11:00am to 12:30pm so it sits after his meme, inside the 9am to 12pm activity peak's tail. 6:30pm Story now ties to the 12:30pm carousel. "CrossFit" allowed on Instagram. Tue/Thu/Sat 7:30am text Reels kept as an experiment until 2026-11-26: keep them only if their median shares and non-follower reach beat the 12:30pm carousels; otherwise cut them. Evidence: 30-day insights to 5 Nov, 33.7k views, 85.4% from followers, 3 external link taps, top 3 posts all meme Reels.
- 2026-11-02: Mandate added. Workout approval dropped. Daily reports stopped (weekly + problems only).

## Slots
Core strategy (from 2026-11-06): Chris's meme Reel at about 9:30am (posted by him, not queued here), then one Claude feed post and one Story every day. Extra weekly posts sit on top and never replace a core slot. All Claude posts are scheduled through Buffer the evening before.
Core, every day:
- About 9:30am: Chris's meme Reel (his slot; never queue anything for it).
- 12:30pm: coaching insight carousel (slot DATE-am). Coaching content needs swipe-at-your-own-pace, and saves are its job.
- 6:30pm: Story tied to the 12:30pm carousel (slot DATE-story).
- 4:00pm relatable carousel (slot DATE): PAUSED from 2026-11-06. Do not queue it. The weekly review may bring it back only with evidence.
Extras:
- Mon 5:30am: workout of the week Story (slot DATE-wod).
- Mon 7:30am: workout walkthrough Reel, timer format (slot DATE-early). Goes with the workout.
- Tue, Thu, Sat 7:30am: short punchy Reel (slot DATE-early).
- Wed 8:00pm: "Rate this workout" Story (slot DATE-rate).
All feed posts on the same day (12:30pm carousel and any 7:30am Reel) must cover different topics.
Updated 2026-10-15 after auditing 150 posts: relatable gym-culture carousels and Reels (Apr to Jul)
had a median reach of about 1,280; long educational posts with site links (Sep to Oct) had about 220.

## 12:30pm slot: coaching insight carousel, every day
- One sharp coach-level observation per carousel (form breakdowns, plateau causes, recovery mistakes, programming logic such as deloads, retests and energy systems, warm-ups, pacing, scaling). One idea per slide, no lecture.
- Format: tools/carousel.py, 5 to 7 slides: cover hook, 3 to 5 content slides (tag, title under ~40 characters, body under ~120), end slide with a CTA. Render to posts/DATE-am/ and queue {"images": [slide URLs in order], "proof": false}.
- The hook must be specific and land on the cover.
- End the caption with "Save this for your next session." then a permitted CTA.
- Rotate themes across the week so no theme repeats within 7 days. Don't repeat the topic of that day's 7:30am Reel.

## Reels: short and punchy (from 2026-10-28)
- Every Reel uses tools/punchy_reel.py (read its docstring). Rule: 2 to 6 words on screen at a time, nothing the viewer has to pause to read. 5 to 15 seconds (hard limit 25). The first scene (hook) holds at least 2 seconds so the Buffer cover frame at 1.5s shows it.
- Five formats:
  1. oneliner: setup, then punchline, no end card so it loops. 5 to 7 seconds. Best home for a provocative hook.
  2. timer: a big clock with one short thought per step (a workout told minute by minute).
  3. flash: "Pause on a random frame" / "Screenshot" list of 6 to 10 types or habits, 0.6s each.
  4. counter: a number ticks to each value (splits, reps, rounds, kilos), then one coaching punchline.
  5. versus: this or that, 4 to 6 pairs.
- Never the same format in two Reels in a row, and use at least three different formats each week. Hooks and topics follow the same rules as feed posts (different topic from that day's 12:30pm carousel).
- Old long-beat text Reels (tools/reel.py) are retired. Don't use them.

## Extra 7:30am Reels (slot DATE-early): Mon, Tue, Thu, Sat
- Tue/Thu/Sat Reels are on trial until 2026-11-26 (see Change log). Lean to coaching Reels (counter, oneliner with a real coaching point); Chris covers gym-culture humour with his memes.
- Rendered to posts/DATE-early/reel.mp4 with tools/punchy_reel.py, caption ops/captions/DATE-early.txt. Caption: hook, at most 2 short lines, then a permitted CTA ("Save this for your next session." only when the Reel teaches something).
- Mon: "This week's workout" in the timer format: the workout of the week told as a pacing plan, minute by minute (e.g. "0:00 Steady. Not a sprint." "6:00 Break the pull-ups early." "13:00 Now go."). Label "This week's workout". Hook names the workout.
- Tue, Thu, Sat: a punchy Reel in any format except timer (Mon owns it), rotating so no format repeats that week. Mix gym-culture humour (oneliner, flash, versus) with at least one coaching Reel a week (counter, or a oneliner with a real coaching point). Movement-of-the-week teaching (setup, common mistake, scaled version) moves to the 11am carousel as a theme when wanted.

## Monday 5:30am: workout of the week Story
- One workout a week, Mondays only. Not daily: Chris's full programming stays in his product, so never post a week plan or a program, only this one session.
- Card from tools/workout.py, rendered to posts/DATE-wod/01.png and queued as ops/queue/DATE-wod.json ({"images": [URL]}) with NO caption file.
- Claude writes the workout. Rules:
  - Built for a general group class of mixed ability: a strength piece (15 to 20 minutes) and a metcon (8 to 20 minutes, always with a time cap).
  - Strength: submaximal sets only (for example 5 x 3 @ 75 to 82%, or build to a heavy 3 that still moves well). Never a 1RM test or anything to failure.
  - Metcon: common equipment only (barbell, dumbbells, kettlebells, rower, bike, pull-up bar, box, wall ball, skipping rope). Rx loads in kg as male/female (e.g. 43/30kg) plus one scaling line. No high-rep heavy Olympic lifts under fatigue, no high-skill gymnastics in large sets.
  - Alternate emphasis week to week (squat, hinge, press, pull, mixed) and the metcon format (for time, AMRAP, EMOM, intervals). Check the last 8 specs/*-wod.json so nothing repeats.
  - One "feel" line with the intended stimulus and a target time or score, one "Scale:" line, and "Reply with your time." (or "your score" / "your rounds").
- No approval needed (from 2026-11-02). The Sunday evening run writes the workout, renders the card and the 7:30am walkthrough Reel, checks both, and queues ops/queue/DATE-wod.json and ops/queue/DATE-early.json (caption ops/captions/DATE-early.txt) with the core Monday posts. The workout rules above still apply in full.

## 4pm slot: weekly rotation (PAUSED from 2026-11-06, kept for reference)
- Mon: Relatable gym culture carousel ("that person in class", coach's-eye humour).
- Tue: Relatable gym culture carousel.
- Wed: Second-person story carousel ("You walk in at 5:05am. The whiteboard says..."). Never invent first-person events as if they happened to Chris.
- Thu: "Which slide is you?" carousel.
- Fri: Relatable gym culture carousel.
- Sat: "Which slide is you?" carousel (class types, workout moments, excuses). The format that reached 121K.
- Sun: Relatable gym culture carousel.
- Proof post: about 1 in 20 posts (roughly one every 10 days) replaces a 12:30pm slot with a real product artifact, only when genuine data exists. Only proof posts may mention kenkoperformance.com (use --proof).

## 6:30pm Story, every day
- One 1080x1920 card from tools/story.py, queued as ops/queue/DATE-story.json ({"images": [URL]}) with NO caption file.
- Buffer auto-publishes Stories only without stickers, polls, links, music or captions, so the card itself asks for a DM reply: a quick question tied to that day's 12:30pm carousel ("Which one are you?", "Which fault is yours?") with 2 to 4 lettered options and "Reply with A, B or C." DM replies are the engagement signal we want.
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
- Punch at habits, myths and gym culture, never at people: nothing mean about beginners, bodies, injuries, other gyms, coaches or named athletes. No health scare claims. Brand rules still apply (no emojis, no em dashes).
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
- "CrossFit" is allowed on Instagram (never in the Kenko app); no affiliation claims or logos.
- Faceless: no people, no faces. Text-on-dark graphics only.
- CTAs: "Follow for more" / "Tag a friend" / "Tag a training partner". Never "Download".
- No motivational, mindset, "new week energy" or inspirational quote posts.
- Humour is affectionate, never mean about beginners, bodies or injuries.
- Premium, confident, no-fluff tone. Coach talking to athletes.

## Weekly review: what to measure (from 2026-11-05)
- Lead with non-follower reach, shares, saves, profile visits and external link taps. Followers are inflated by bought accounts, so follower count and follower reach are not success measures.
- Compare Chris's meme Reels (his posts, no queue file) against Claude's posts every week, and report the gap.
- In the Monday report, give Chris 7 meme caption ideas for the week, modelled on his best memes from the previous week (relatable class moments, specific times and people, "when you..." setups). Ideas only; he picks the clip and posts it.
- 2026-11-26: decide on the Tue/Thu/Sat Reel trial (keep only if they beat the 12:30pm carousels on median shares and non-follower reach).

## Look
- 1080x1350 slides, #0a0a0a background, white text, #00FF87 accent, Inter.
- Carousels: tools/carousel.py. Reels: tools/punchy_reel.py (1080x1920 MP4). Stories: tools/story.py (1080x1920 PNG). Workout card: tools/workout.py (1080x1920 PNG). Single cards: tools/render.py.

## Files (all under ops/ in kasamasuki/kenko-content; this repo is public, so nothing secret goes here)
- captions/YYYY-MM-DD.txt  caption for each post (read these to avoid repeating topics)
- queue/SLOT.json          slide URLs ({"images": [...]}) or a Reel ({"video": URL}); pushing it runs the schedule-post Action
- posted.log               date, Buffer post id, due time, first image URL, image count
- weekly-summary.md        last week's reach, shares, saves, best and worst post (fetch-history Action, Mondays)
- BUFFER_KEY secret        Buffer API key, stored as a GitHub Actions secret (never print or commit it). Expires 2027-10-15.
- post_to_buffer.py        schedules the post; refuses duplicates and rule-breaking captions
