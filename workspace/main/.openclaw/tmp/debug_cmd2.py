import subprocess, json, sys

# Set console to UTF-8, then call openclaw
cmd = [
    "cmd", "/c",
    "chcp 65001 > nul && openclaw agent --agent main --message ping --json --local --session-key agent:main:debug-cmd-002 --timeout 60"
]

try:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=120)
    print("EXIT CODE:", r.returncode)
    if r.stdout.strip():
        # Try to parse as JSON, but chcp also outputs stuff
        # Find the JSON part
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith('{'):
                try:
                    data = json.loads(line)
                    texts = [p['text'] for p in data.get('payloads', []) if p.get('text')]
                    print("AGENT REPLY:", texts)
                except:
                    pass
        if not r.stdout.strip().startswith('{'):
            # Check the raw output
            print("STDOUT[:500]:", r.stdout[:500])
    if r.stderr:
        print("STDERR[:300]:", r.stderr[:300])
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
