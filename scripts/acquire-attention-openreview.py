#!/usr/bin/env python3
"""Acquire immutable OpenReview submission records with provenance and rate-limit safety."""
import argparse, hashlib, json, pathlib, time, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone

INVITATIONS = {
  2017:["ICLR.cc/2017/conference/-/submission","ICLR.cc/2017/Conference/-/Blind_Submission"],
  2018:["ICLR.cc/2018/Conference/-/Blind_Submission"],
  2019:["ICLR.cc/2019/Conference/-/Blind_Submission"],
  2020:["ICLR.cc/2020/Conference/-/Blind_Submission"],
  2021:["ICLR.cc/2021/Conference/-/Blind_Submission"],
  2022:["ICLR.cc/2022/Conference/-/Blind_Submission"],
}
BASE="https://api.openreview.net/notes"

def sha256(b): return hashlib.sha256(b).hexdigest()

def fetch(params, retries=7):
    url=BASE+"?"+urllib.parse.urlencode(params)
    for attempt in range(retries):
        req=urllib.request.Request(url,headers={"User-Agent":"AgalmicResearch-AttentionAllocation/0.1"})
        try:
            with urllib.request.urlopen(req,timeout=60) as r:
                return r.read(), dict(r.headers), url
        except urllib.error.HTTPError as e:
            if e.code not in (429,500,502,503,504): raise
            wait=float(e.headers.get("Retry-After") or min(120,2**attempt))
            time.sleep(wait)
    raise RuntimeError(f"retry budget exhausted: {url}")

def acquire_year(year,out,limit=1000):
    errors=[]
    for invitation in INVITATIONS[year]:
        try:
            first,headers,url=fetch({"invitation":invitation,"limit":1})
            probe=json.loads(first)
            if "notes" not in probe: raise RuntimeError("response has no notes")
            break
        except Exception as e: errors.append({"invitation":invitation,"error":repr(e)})
    else: return {"year":year,"status":"blocked","errors":errors}

    rawdir=out/"raw"/str(year); rawdir.mkdir(parents=True,exist_ok=True)
    offset=0; count=0; pages=[]
    while True:
        body,headers,url=fetch({"invitation":invitation,"limit":limit,"offset":offset})
        obj=json.loads(body); notes=obj.get("notes",[])
        page=rawdir/f"notes-{offset:06d}.json"
        page.write_bytes(body)
        pages.append({"path":str(page),"sha256":sha256(body),"url":url,"count":len(notes)})
        count += len(notes)
        if len(notes)<limit: break
        offset += len(notes); time.sleep(1)
    return {"year":year,"status":"acquired","invitation":invitation,"count":count,"pages":pages,"probe_errors":errors}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--out",default="research/attention_allocation/data")
    p.add_argument("--years",nargs="+",type=int,default=list(range(2017,2023))); p.add_argument("--limit",type=int,default=1000)
    a=p.parse_args(); out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=True)
    manifest={"schema_version":"0.1","source":"OpenReview API","acquired_at":datetime.now(timezone.utc).isoformat(),"years":[]}
    for y in a.years:
        if y not in INVITATIONS: raise SystemExit(f"unsupported year {y}")
        manifest["years"].append(acquire_year(y,out,a.limit))
    payload=json.dumps(manifest,indent=2,sort_keys=True)+"\n"
    (out/"manifest.json").write_text(payload)
    print(payload)

if __name__=="__main__": main()
