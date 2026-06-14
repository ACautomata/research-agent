$lines = Get-Content 'D:\Code\= =\research-agent\benchmarks\idea-generate\qa.jsonl' -Encoding UTF8
$total = 0
foreach ($line in $lines) {
    $t = $line.Trim()
    if ($t -ne '' -and -not $t.StartsWith('#')) {
        $total++
    }
}
Write-Output "=== QA Summary ==="
Write-Output "Total QAs: $total"
Write-Output ""

$types = @{}
$judges = @{}
foreach ($line in $lines) {
    $t = $line.Trim()
    if ($t -eq '' -or $t.StartsWith('#')) { continue }
    $qa = $t | ConvertFrom-Json
    $type = if ($qa.task_type) { $qa.task_type } else { '(none)' }
    $judge = if ($qa.judge) { $qa.judge } else { 'rules' }
    Write-Output "$($qa.qa_id) | $type | $judge | w=$($qa.weight)"
    if (-not $types.ContainsKey($type)) { $types[$type] = 0 }
    $types[$type]++
    if (-not $judges.ContainsKey($judge)) { $judges[$judge] = 0 }
    $judges[$judge]++
}

Write-Output ""
Write-Output "=== By Task Type ==="
foreach ($k in $types.Keys) { Write-Output "  $k = $($types[$k])" }

Write-Output ""
Write-Output "=== By Judge Mode ==="
foreach ($k in $judges.Keys) { Write-Output "  $k = $($judges[$k])" }
