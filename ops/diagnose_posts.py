#!/usr/bin/env python3
"""Read-only: print Buffer status and any error for recent posts on the channel (no key printed).
Run by the diagnose-posts Action (workflow_dispatch)."""
import json, os, urllib.request
ORG, CH = "6a8b76dfdd8fa727018fa461", "6a97e322065799be4671f725"
KEY = os.environ["BUFFER_KEY"]
def call(q, v=None):
    r = urllib.request.Request("https://api.buffer.com", method="POST",
        data=json.dumps({"query": q, "variables": v or {}}).encode(),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(r, timeout=60))
    except urllib.error.HTTPError as e:
        return {"httpError": e.code, "body": e.read().decode()[:1500]}
# 1. Which fields does Post have? (so we can ask for the error ones)
t = call('{ __type(name:"Post"){ fields{ name type{ name kind ofType{ name kind } } } } }')
fields = [f["name"] for f in ((t.get("data") or {}).get("__type") or {}).get("fields") or []]
print("Post fields:", fields or json.dumps(t)[:1500])
scalar = {"id", "status", "dueAt", "sentAt", "text", "error", "errorMessage", "failedAt", "externalLink", "via", "schedulingType", "createdAt", "updatedAt", "isCustomScheduled"}
want = [f for f in fields if f in scalar or "error" in f.lower() or "fail" in f.lower() or "notif" in f.lower()]
sel = " ".join(want or ["id", "status", "dueAt", "sentAt"])
# expand object-typed error fields generically
objs = {f["name"]: f for f in ((t.get("data") or {}).get("__type") or {}).get("fields") or []}
def sub(name):
    f = objs.get(name); k = f["type"]["kind"] if f else "SCALAR"
    k = f["type"]["ofType"]["kind"] if k in ("NON_NULL", "LIST") and f["type"].get("ofType") else k
    if k == "OBJECT":
        tn = f["type"]["name"] or f["type"]["ofType"]["name"]
        st = call('{ __type(name:"%s"){ fields{ name type{ kind ofType{ kind } } } } }' % tn)
        inner = [x["name"] for x in st["data"]["__type"]["fields"] if x["type"]["kind"] in ("SCALAR","ENUM") or (x["type"].get("ofType") or {}).get("kind") in ("SCALAR","ENUM")]
        return name + "{ " + " ".join(inner) + " }"
    return name
sel = " ".join(sub(f) for f in (want or ["id", "status", "dueAt", "sentAt"]))
for status in ["error", "sent", "scheduled", "needs_approval", "draft"]:
    q = 'query{ posts(first:20, input:{organizationId:"%s", filter:{status:[%s], channelIds:["%s"]}}){ edges{ node{ %s } } } }' % (ORG, status, CH, sel)
    d = call(q)
    if "errors" in d or "httpError" in d:
        print(f"[{status}] query error:", json.dumps(d)[:800]); continue
    nodes = [e["node"] for e in d["data"]["posts"]["edges"]]
    print(f"\n[{status}] {len(nodes)} posts")
    for n in sorted(nodes, key=lambda n: n.get("dueAt") or "", reverse=True)[:20]:
        if "text" in n and n["text"]: n["text"] = n["text"].splitlines()[0][:50]
        print(json.dumps(n))
