$report = Get-Content 'D:\Code\= =\research-agent\benchmarks\idea-generate\bench-report.json' -Encoding UTF8 | ConvertFrom-Json
$result = $report.results[0]
Write-Output "qa_id: $($result.qa_id)"
Write-Output "score: $($result.score)"
Write-Output "pass: $($result.pass)"
Write-Output "rationale: $($result.rationale)"
Write-Output "elapsed: $($result.elapsed_seconds)s"
Write-Output "--- raw_output (first 600 chars) ---"
$raw = $result.raw_output
Write-Output ($raw.Substring(0, [Math]::Min(600, $raw.Length)))
