#!/usr/bin/env python3
import re
import sys

PATTERNS = [
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "github_pat_****REDACTED****"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), "gh*_****REDACTED****"),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{12,}"), r"\1****REDACTED****"),
    (re.compile(r"(?i)(access_token\s*[=:]\s*)[^\s&'\"]+"), r"\1****REDACTED****"),
    (re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)[^\s&'\"]+"), r"\1****REDACTED****"),
    (re.compile(r"(?i)(secret\s*[=:]\s*)[^\s&'\"]+"), r"\1****REDACTED****"),
    (re.compile(r"(?i)(token\s*[=:]\s*)[^\s&'\"]+"), r"\1****REDACTED****"),
    (re.compile(r"(?i)(cookie\s*[:=]\s*)[^\n]+"), r"\1****REDACTED****"),
    (re.compile(r"(?i)(JSESSIONID=)[^;\s]+"), r"\1****REDACTED****"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"), "-----BEGIN PRIVATE KEY-----\n****REDACTED****\n-----END PRIVATE KEY-----"),
    (re.compile(r"octo_loop_[A-Za-z0-9._-]{8,}"), "octo_loop_****REDACTED****"),
    (re.compile(r"app_[A-Za-z0-9._-]{8,}"), "app_****REDACTED****"),
    (re.compile(r"bf_[A-Za-z0-9._-]{8,}"), "bf_****REDACTED****"),
    (re.compile(r"uk_[A-Za-z0-9._-]{8,}"), "uk_****REDACTED****"),
]

def sanitize(text: str) -> str:
    out = text
    for pattern, repl in PATTERNS:
        out = pattern.sub(repl, out)
    return out

if __name__ == "__main__":
    data = sys.stdin.read() if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    sys.stdout.write(sanitize(data))
