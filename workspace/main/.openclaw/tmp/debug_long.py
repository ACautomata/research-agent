import subprocess, json, sys

# Test with long prompt containing newlines
long_prompt = (
    "这是一段测试长文本。\n" * 50 +
    "请回复确认你能处理多行文本。"
)

cmd = [
    "openclaw.cmd",
    "agent", "--agent", "main",
    "--message", long_prompt,
    "--json", "--local",
    "--session-key", "agent:main:debug-long-001",
    "--timeout", "120",
    "--model", "deepseek/deepseek-v4-flash"
]

try:
    r = subprocess.run(cmd, capture_output=True, timeout=180)
    stdout_text = r.stdout.decode('utf-8', errors='replace')
    stderr_text = r.stderr.decode('utf-8', errors='replace')
    print("EXIT CODE:", r.returncode)
    for line in stdout_text.splitlines():
        line = line.strip()
        if line.startswith('{'):
            try:
                data = json.loads(line)
                texts = [p['text'] for p in data.get('payloads', []) if p.get('text')]
                print("AGENT REPLY:", texts[0][:200] if texts else "NO TEXT")
                if data.get('meta', {}).get('agentMeta', {}).get('model'):
                    print("MODEL:", data['meta']['agentMeta']['model'])
                break
            except:
                continue
    if stderr_text.strip():
        print("STDERR[:200]:", stderr_text[:200])
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
