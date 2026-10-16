# kenko-content
Image hosting for @coach_chris_kenko Instagram posts

## Scheduling (ops/)
Everything runs on GitHub, no Mac needed.
- ops/PLAYBOOK.md: pillars, rotation, brand rules (source of truth)
- To schedule a post, push `ops/captions/DATE.txt` and `ops/queue/DATE.json`
  (`{"images": [slide URLs in order], "proof": false}`) to main. The schedule-post Action runs
  ops/post_to_buffer.py with the BUFFER_KEY secret and appends the Buffer post id to ops/posted.log.
- The fetch-history Action writes ops/weekly-summary.md every Monday morning.
- The Buffer key expires 2027-10-15: replace the BUFFER_KEY secret before then.
