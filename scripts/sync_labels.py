#!/usr/bin/env python3
"""Sync the exam label set. Requires gh auth and GITHUB_REPO=owner/repo."""
import os, subprocess, sys
LABELS = [
("type:bug","d73a4a","Bug or unexpected behavior"),
("type:feature","a2eeef","Feature request or product improvement"),
("type:question","d876e3","Product or usage question"),
("type:docs","0075ca","Documentation gap or improvement"),
("type:prd","5319e7","PRD related item"),
("type:review","7057ff","Review related item"),
("type:security","b60205","Security or sensitive data related item"),
("priority:P0","b60205","Critical blocker, security risk, or exam-critical issue"),
("priority:P1","d93f0b","High priority"),
("priority:P2","fbca04","Normal priority"),
("priority:P3","cfd3d7","Low priority"),
("status:triage","ededed","Needs initial classification"),
("status:need-info","fbca04","Needs more information"),
("status:accepted","0e8a16","Accepted for processing"),
("status:prd-draft","bfdadc","PRD draft created or in progress"),
("status:in-review","5319e7","In review"),
("status:changes-requested","d93f0b","Changes requested"),
("status:ready","0e8a16","Ready after review"),
("status:wontfix","000000","Closed as not planned or wontfix"),
("status:closed","6a737d","Closed"),
("status:need-human","b60205","Needs human confirmation"),
("source:octo-group","c5def5","Submitted from Octo exam group"),
("source:examiner","c5def5","Submitted or changed by examiner"),
("source:agent","c5def5","Created by agent automation"),
("source:manual","c5def5","Created or updated manually"),
("security:secret-risk","b60205","Potential secret or credential risk"),
("security:sanitized","0e8a16","Sensitive data sanitized"),
("security:needs-human","d93f0b","Security case needs human review"),
("pm:needs-prd","5319e7","Needs PRD drafting"),
("pm:prd-created","5319e7","PRD has been created"),
("pm:review-passed","0e8a16","PRD review passed"),
("pm:review-failed","d93f0b","PRD review failed"),
("pm:revision-done","0e8a16","Revision completed"),
]
repo = os.environ.get("GITHUB_REPO")
if not repo:
    print("GITHUB_REPO is required", file=sys.stderr); sys.exit(2)
existing = subprocess.check_output(["gh","label","list","--repo",repo,"--limit","200","--json","name","--jq",".[].name"], text=True).splitlines()
for name,color,desc in LABELS:
    cmd = ["gh","label","edit" if name in existing else "create",name,"--repo",repo,"--color",color,"--description",desc]
    subprocess.run(cmd, check=True)
    print(("updated" if name in existing else "created")+": "+name)
