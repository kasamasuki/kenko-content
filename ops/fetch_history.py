#!/usr/bin/env python3
"""Download sent Instagram posts with Buffer metrics to post_history.json."""
import json, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ORG, CH = "6a8b76dfdd8fa727018fa461", "6a97e322065799be4671f725"
KEY = os.environ.get("BUFFER_KEY") or open(os.path.join(HERE, "buffer_key.txt")).read().strip()
Q = """query($after:String){ posts(first:50, after:$after, input:{organizationId:"%s",
 filter:{status:[sent], channelIds:["%s"]}}){ edges{ node{ id text dueAt sentAt
 assets{ mimeType } metrics{ type name value unit } metricsUpdatedAt } }
 pageInfo{ hasNextPage endCursor } } }""" % (ORG, CH)
def call(v):
    r = urllib.request.Request("https://api.buffer.com", method="POST",
        data=json.dumps({"query": Q, "variables": v}).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=60))
out, after = [], None
for _ in range(40):
    d = call({"after": after})
    if "errors" in d: print(json.dumps(d["errors"])[:800]); break
    p = d["data"]["posts"]; out += [e["node"] for e in p["edges"]]
    if not p["pageInfo"]["hasNextPage"]: break
    after = p["pageInfo"]["endCursor"]
json.dump(out, open(os.path.join(HERE, "post_history.json"), "w"), indent=1)
print(len(out), "posts saved")
