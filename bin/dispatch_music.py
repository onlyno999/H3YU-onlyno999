#!/usr/bin/env python3
"""H3YU dispatcher: MiniMax Music 3 workflow 2108276969036148738 on RunningHub.
Usage: dispatch_music.py --brief brief.json
brief.json: {"caption": str, "lyrics": str, "seconds": int, "prefix": str, "outdir": str}
Overrides exactly five fields; 42.max_duration and 46.seconds always move together (Iron Rule 1).
Polls until SUCCESS/FAILED (25 min cap), downloads the MP3, writes result.json next to the brief.
"""
import sys, os, json, time, argparse, urllib.request, urllib.error
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request

BASE = "https://www.runninghub.cn"
WF = "2108276969036148738"

def call(path, payload):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "h3yu-dispatch/1.0"}, method="POST")
    add_surrogate_to_request(req, "custom.runninghub", allowed_hosts=["www.runninghub.cn"])
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True)
    a = ap.parse_args()
    brief = json.load(open(a.brief))
    sec = str(int(brief["seconds"]))
    nodes = [
        {"nodeId": "42", "fieldName": "caption", "fieldValue": brief["caption"]},
        {"nodeId": "42", "fieldName": "lyrics", "fieldValue": brief["lyrics"]},
        {"nodeId": "42", "fieldName": "max_duration", "fieldValue": sec},
        {"nodeId": "46", "fieldName": "seconds", "fieldValue": sec},
        {"nodeId": "35", "fieldName": "filename_prefix", "fieldValue": brief["prefix"]},
    ]
    r = call(f"/openapi/v2/run/workflow/{WF}",
             {"nodeInfoList": nodes, "instanceType": "default", "usePersonalQueue": False})
    tid = r.get("taskId")
    if not tid:
        print("DISPATCH_FAILED:", json.dumps(r, ensure_ascii=False)[:500]); sys.exit(1)
    print("taskId:", tid, flush=True)
    outdir = brief.get("outdir") or os.path.dirname(os.path.abspath(a.brief))
    os.makedirs(outdir, exist_ok=True)
    deadline = time.time() + 25 * 60
    final = None
    while time.time() < deadline:
        q = call("/openapi/v2/query", {"taskId": tid})
        st = q.get("status")
        print("status:", st, flush=True)
        if st in ("SUCCESS", "FAILED"):
            final = q; break
        time.sleep(20)
    if not final:
        print("TIMEOUT"); sys.exit(2)
    with open(os.path.join(outdir, "result.json"), "w") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    if final.get("status") != "SUCCESS":
        print("TASK_FAILED:", json.dumps(final, ensure_ascii=False)[:500]); sys.exit(3)
    url = final["results"][0]["url"]
    mp3 = os.path.join(outdir, brief["prefix"] + ".mp3")
    urllib.request.urlretrieve(url, mp3)
    print("DOWNLOADED:", mp3)

if __name__ == "__main__":
    main()
