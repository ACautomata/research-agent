$report = Get-Content 'D:\Code\= =\research-agent\benchmarks\idea-generate\bench-report.json' -Encoding UTF8 | ConvertFrom-Json
$r = $report.results[0]
Write-Output ("qa_id: " + $r.qa_id)
Write-Output ("score: " + $r.score)
$raw = $r.raw_output
$head = $raw.Substring(0, [Math]::Min(300, $raw.Length))
Write-Output ("head: " + $head)
