$promptFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\prompt_QA-001.txt'
$outFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_direct.txt'
$prompt = Get-Content $promptFile -Raw -Encoding UTF8
Write-Output ("Prompt length: " + $prompt.Length)
# Call openclaw and capture raw output
$output = openclaw agent --agent main --message $prompt --json --local --session-key "agent:main:bench-direct-test-001" --timeout 120 --model "deepseek/deepseek-v4-flash" 2>&1
$output | Out-File -FilePath $outFile -Encoding UTF8
Write-Output ("Output saved to: " + $outFile)
$size = (Get-Item $outFile).Length
Write-Output ("Output size: " + $size + " bytes")
