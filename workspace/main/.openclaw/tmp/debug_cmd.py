import subprocess, json, sys

# Test with direct exe/cmd call using list args
prompt = "ping"  # simple test first

cmd = [
    "openclaw.cmd",
    "agent",
    "--agent", "main",
    "--message", prompt,
    "--json", "--local",
    "--session-key", "agent:main:debug-cmd-001",
    "--timeout", "60"
]

try:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=120)
    print("EXIT CODE:", r.returncode)
    if r.stdout.strip():
        data = json.loads(r.stdout)
        texts = [p['text'] for p in data.get('payloads', []) if p.get('text')]
        print("AGENT REPLY:", texts)
    else:
        print("NO STDOUT")
    print("STDERR[:300]:", r.stderr[:300])
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
