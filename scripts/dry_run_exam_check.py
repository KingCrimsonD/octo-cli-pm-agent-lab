#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
repo = Path(__file__).resolve().parents[1]
checks = []
def ok(name, cond):
    checks.append((name, bool(cond)))
required = ["README.md","EXAM_GUIDE.md","SECURITY.md","AGENT_RULES.md","LABEL_SYSTEM.md","CRON_SYSTEM.md","PM_WORKFLOW.md"]
for f in required:
    ok(f"exists:{f}", (repo/f).exists())
for i in range(1,10):
    ok(f"knowledge:{i}", any((repo/"knowledge").glob(f"{i:02d}-*.md")))
res = subprocess.run([sys.executable, str(repo/"scripts"/"verify_citations.py")], cwd=repo, text=True, capture_output=True)
ok("citations_valid", res.returncode == 0)
ok("env_not_tracked", ".env" not in subprocess.check_output(["git","ls-files"], cwd=repo, text=True).splitlines())
ok("cron_log_exists", (repo/"logs"/"cron-runs.jsonl").exists())
failed = [name for name, passed in checks if not passed]
print(json.dumps({"status":"failed" if failed else "success", "failed": failed, "checks": dict(checks)}, ensure_ascii=False, indent=2))
sys.exit(1 if failed else 0)
