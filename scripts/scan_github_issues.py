#!/usr/bin/env python3
"""Minimal cron scanner skeleton for the exam demand pool.
It records runs and detects updated issues. External group reporting should be wired by the Agent runtime.
"""
import json, os, subprocess
from datetime import datetime, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
state_path = repo_root / "state" / "last_scan.json"
cron_log = repo_root / "logs" / "cron-runs.jsonl"
sync_log = repo_root / "logs" / "sync-events.jsonl"
repo = os.environ.get("GITHUB_REPO", "KingCrimsonD/octo-cli-pm-agent-lab")
now = datetime.now(timezone.utc).isoformat()
try:
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
except json.JSONDecodeError:
    state = {}
last = state.get("last_scan")
cmd = ["gh", "issue", "list", "--repo", repo, "--state", "all", "--limit", "100", "--json", "number,title,state,updatedAt,labels,url"]
items = json.loads(subprocess.check_output(cmd, text=True))
changed = [it for it in items if not last or it.get("updatedAt", "") > last]
actions = []
for it in changed:
    labels = [l.get("name") for l in it.get("labels", [])]
    event = {"time": now, "event": "issue_seen", "issue": it["number"], "title": it["title"], "state": it["state"], "labels": labels, "url": it["url"]}
    sync_log.parent.mkdir(parents=True, exist_ok=True)
    with sync_log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    actions.append(f"issue_seen:{it['number']}")
state_path.write_text(json.dumps({"last_scan": now}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
record = {"time": now, "job": "github-issue-sync", "status": "success", "checked_since": last, "changes_found": len(changed), "actions": actions}
cron_log.parent.mkdir(parents=True, exist_ok=True)
with cron_log.open("a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
print(json.dumps(record, ensure_ascii=False))
