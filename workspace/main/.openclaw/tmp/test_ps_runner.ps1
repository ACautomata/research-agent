$base = "D:\Code\= =\research-agent"
$promptPath = Join-Path $base "benchmarks\idea-generate\.bench-temp\prompt_QA-001.txt"
$null = New-Item -ItemType Directory -Force -Path (Split-Path $promptPath -Parent)
Set-Content -Path $promptPath -Value "line 1`nline 2`nline 3" -Encoding UTF8
$prompt = Get-Content $promptPath -Raw -Encoding UTF8
Write-Output ("PROMPT LENGTH: " + $prompt.Length + " bytes")
$result = openclaw agent --agent main --message $prompt --json --local --session-key "agent:main:bench-ps-test-003" --timeout 120 --model "deepseek/deepseek-v4-flash" 2>$null
$parsed = $result | ConvertFrom-Json
$reply = $parsed.payloads[0].text
Write-Output ("AGENT REPLY: " + $reply)
