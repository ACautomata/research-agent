$report = Get-Content 'D:\Code\= =\research-agent\benchmarks\idea-generate\bench-report.json' -Encoding UTF8 | ConvertFrom-Json
Write-Output "=== idea-generate Benchmark Report ==="
Write-Output "Model: $($report.model)  |  Passed: $($report.passed)/$($report.total)  |  Pass rate: $($report.pass_rate)  |  Avg score: $($report.avg_score)"
Write-Output ""
Write-Output "Results breakdown:"
foreach ($r in $report.results) {
    $status = if ($r.pass) { "+" } else { "-" }
    $rStr = if ($r.rationale.Length -gt 80) { $r.rationale.Substring(0,80) + "..." } else { $r.rationale }
    Write-Output ("  [$status] $($r.qa_id) | $($r.task_type) | score=$($r.score) | $($r.elapsed_seconds)s | $rStr")
}
