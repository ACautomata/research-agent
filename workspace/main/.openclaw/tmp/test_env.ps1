$promptFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\prompt_QA-001.txt'
$outFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_env.txt'
$env:BENCH_PROMPT = Get-Content $promptFile -Raw -Encoding UTF8
Write-Output ("Prompt length: " + $env:BENCH_PROMPT.Length)
# Call openclaw with prompt via env var
$output = openclaw agent --agent main --message $env:BENCH_PROMPT --json --local --session-key "agent:main:bench-env-test-001" --timeout 120 --model "deepseek/deepseek-v4-flash" 2>&1
$output | Out-File -FilePath $outFile -Encoding UTF8
$size = (Get-Item $outFile).Length
Write-Output ("Output size: " + $size + " bytes")
Remove-Item Env:BENCH_PROMPT -ErrorAction SilentlyContinue
