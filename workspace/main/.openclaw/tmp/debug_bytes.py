import subprocess, json, sys

# Spawn with bytes capture, manually decode
cmd = [
    "openclaw.cmd",
    "agent", "--agent", "main",
    "--message", "ping",
    "--json", "--local",
    "--session-key", "agent:main:debug-bytes-001",
    "--timeout", "60"
]

try:
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    # r.stdout is bytes - try to find and decode JSON
    stdout_text = r.stdout.decode('utf-8', errors='replace')
    stderr_text = r.stderr.decode('utf-8', errors='replace')
    print("EXIT CODE:", r.returncode)
    if stdout_text.strip():
        # Find JSON payload
        for line in stdout_text.splitlines():
            line = line.strip()
            if line.startswith('{'):
                try:
                    data = json.loads(line)
                    texts = [p['text'] for p in data.get('payloads', []) if p.get('text')]
                    print("AGENT REPLY:", texts)
                    break
                except:
                    continue
        else:
            print("STDOUT[:500]:", stdout_text[:500])
    if stderr_text.strip():
        print("STDERR[:300]:", stderr_text[:300])
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
