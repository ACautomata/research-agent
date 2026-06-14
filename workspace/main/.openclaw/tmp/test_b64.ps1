$promptFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\prompt_QA-001.txt'
$outFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_b64.txt'

# Read prompt and base64 encode it
$prompt = Get-Content $promptFile -Raw -Encoding UTF8
$bytes = [System.Text.Encoding]::UTF8.GetBytes($prompt)
$b64 = [Convert]::ToBase64String($bytes)

# Pass b64 string (single-line, no newlines) to openclaw
$output = openclaw agent --agent main --message $b64 --json --local --session-key "agent:main:bench-b64-test-001" --timeout 120 --model "deepseek/deepseek-v4-flash" 2>&1
$output | Out-File -FilePath $outFile -Encoding UTF8
$size = (Get-Item $outFile).Length
Write-Output ("B64 output size: " + $size + " bytes")
