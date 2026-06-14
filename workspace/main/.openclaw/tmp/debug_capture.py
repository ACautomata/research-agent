"""Debug: save stdout and stderr separately to files."""
import subprocess, json, sys, os, time

NODE_EXE = r"C:\Program Files\nodejs\node.exe"
APPDATA = os.environ.get("APPDATA", "")
OPENCLAW_MJS = os.path.join(APPDATA, "npm", "node_modules", "openclaw", "openclaw.mjs")
PROMPT = "ping"
SESSION_KEY = "agent:main:debug-capture-test"

args = [
    NODE_EXE,
    OPENCLAW_MJS,
    "agent",
    "--agent", "main",
    "--message", PROMPT,
    "--json", "--local",
    "--session-key", SESSION_KEY,
    "--timeout", "60",
    "--model", "deepseek/deepseek-v4-flash",
]

# Use PIPE but also use a timeout
proc = subprocess.run(args, capture_output=True, timeout=120)

# Save to files
out_path = r"D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_capture_stdout.txt"
err_path = r"D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_capture_stderr.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write(proc.stdout.decode("utf-8", errors="replace"))
with open(err_path, "w", encoding="utf-8") as f:
    f.write(proc.stderr.decode("utf-8", errors="replace"))

print(f"stdout: {len(proc.stdout)} bytes -> {out_path}")
print(f"stderr: {len(proc.stderr)} bytes -> {err_path}")
print(f"exit code: {proc.returncode}")

# Parse stdout
stdout_text = proc.stdout.decode("utf-8", errors="replace")
for line in stdout_text.splitlines():
    line = line.strip()
    if line.startswith("{"):
        try:
            data = json.loads(line)
            payloads = data.get("payloads", [])
            print(f"JSON payloads count: {len(payloads)}")
            if payloads:
                for i, p in enumerate(payloads):
                    text = p.get("text", "")
                    print(f"  payload[{i}]: {text[:100]}")
            else:
                # Check meta
                meta = data.get("meta", {})
                print(f"  meta.finalAssistantVisibleText: {meta.get('finalPromptText', 'N/A')[:100]}")
                print(f"  meta.agentMeta.model: {meta.get('agentMeta', {}).get('model', 'N/A')}")
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}")
