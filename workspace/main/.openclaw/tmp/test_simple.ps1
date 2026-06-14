# Test with simple single-line message
$outFile = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_simple.txt'
$output = openclaw agent --agent main --message "testing 123" --json --local --session-key "agent:main:bench-simple-test" --timeout 60 --model "deepseek/deepseek-v4-flash" 2>&1
$output | Out-File -FilePath $outFile -Encoding UTF8
$size = (Get-Item $outFile).Length
Write-Output ("Simple message output size: " + $size + " bytes")

# Test with single-line but long message
$longLine = "test " * 200
$outFile2 = 'D:\Code\= =\research-agent\benchmarks\idea-generate\.bench-temp\debug_longline.txt'
$output2 = openclaw agent --agent main --message $longLine --json --local --session-key "agent:main:bench-longline-test" --timeout 60 --model "deepseek/deepseek-v4-flash" 2>&1
$output2 | Out-File -FilePath $outFile2 -Encoding UTF8
$size2 = (Get-Item $outFile2).Length
Write-Output ("Long single-line output size: " + $size2 + " bytes")
