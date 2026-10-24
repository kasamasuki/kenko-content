# kenko-content
Image hosting for @coach_chris_kenko Instagram posts

## Scheduling (ops/)
Everything runs on GitHub, no Mac needed.
- ops/PLAYBOOK.md: pillars, rotation, brand rules (source of truth)
- Each day: slot `DATE-am` (11am Reel), slot `DATE` (4pm carousel), slot `DATE-story` (6:30pm Story, queue file only, no caption). Melbourne time.
- To schedule a post, push `ops/captions/SLOT.txt` and `ops/queue/SLOT.json`
  (`{"images": [slide URLs in order], "proof": false}`, or `{"video": "...mp4 URL"}` for a Reel) to main. The schedule-post Action runs
  ops/post_to_buffer.py with the BUFFER_KEY secret and appends the Buffer post id to ops/posted.log.
- Reels: `python3 tools/reel.py specs/SLOT.json posts/SLOT/reel.mp4` renders a faceless text Reel from a carousel spec.
  Test any queue change with `python3 ops/run_queue.py --dry-run` (prints the Buffer payload, posts nothing).
- The fetch-history Action writes ops/weekly-summary.md every Monday morning.
- The Buffer key expires 2027-10-15: replace the BUFFER_KEY secret before then.
