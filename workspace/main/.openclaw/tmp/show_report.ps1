$report = Get-Content 'D:\Code\= =\research-agent\benchmarks\idea-generate\bench-report.json' -Encoding UTF8 | ConvertFrom-Json
Write-Output ("=== Benchmark Report: " + $report.benchmark + " ===")
Write-Output ("Model: " + $report.model)
Write-Output ("Agent: " + $report.agent)
Write-Output ("Total: " + $report.total)
Write-Output ("Passed: " + $report.passed)
Write-Output ("Pass rate: " + $report.pass_rate)
Write-Output ("Avg score: " + $report.avg_score)
Write-Output ""
Write-Output "=== By Task Type ==="
$typeStats = @{}
foreach ($r in $report.results) {
    $t = $r.task_type
    if (-not $typeStats.ContainsKey($t)) { $typeStats[$t] = @{total=0; passed=0; scoreSum=0.0} }
    $typeStats[$t].total++
    if ($r.pass) { $typeStats[$t].passed++ }
    $typeStats[$t].scoreSum += $r.score
}
foreach ($t in ($typeStats.Keys | Sort-Object)) {
    $s = $typeStats[$t]
    $avg = [math]::Round($s.scoreSum / $s.total, 3)
    Write-Output ("  $t : $($s.passed)/$($s.total) passed, avg=$avg")
}
Write-Output ""
Write-Output "=== By Judge Mode ==="
$judgeStats = @{}
foreach ($r in $report.results) {
    $j = "agent-judge"
    foreach ($qa_line in (Get-Content 'D:\Code\= =\research-agent\benchmarks\idea-generate\qa.jsonl' -Encoding UTF8)) {
        if ($qa_line.Trim() -ne "" -and -not $qa_line.StartsWith("#")) {
            $qa_data = $qa_line | ConvertFrom-Json
            if ($qa_data.qa_id -eq $r.qa_id) {
                $j = if ($qa_data.judge -eq "agent") { "agent-judge" } else { "rules-judge" }
                break
            }
        }
    }
    if (-not $judgeStats.ContainsKey($j)) { $judgeStats[$j] = @{total=0; passed=0; scoreSum=0.0} }
    $judgeStats[$j].total++
    if ($r.pass) { $judgeStats[$j].passed++ }
    $judgeStats[$j].scoreSum += $r.score
}
foreach ($j in ($judgeStats.Keys | Sort-Object)) {
    $s = $judgeStats[$j]
    $avg = [math]::Round($s.scoreSum / $s.total, 3)
    Write-Output ("  $j : $($s.passed)/$($s.total) passed, avg=$avg")
}
