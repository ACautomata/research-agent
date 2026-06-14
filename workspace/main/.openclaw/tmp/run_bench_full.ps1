$env:PYTHONUTF8 = "1"
$env:BENCH_MODEL = "deepseek/deepseek-v4-flash"
$base = "D:\Code\= =\research-agent"
Write-Output "Starting full benchmark run at $(Get-Date -Format 'HH:mm:ss')"
$t0 = Get-Date
python (Join-Path $base "workspace\bench_runner.py")
$t1 = Get-Date
Write-Output "Finished at $(Get-Date -Format 'HH:mm:ss')"
Write-Output ("Total time: " + [math]::Round(($t1-$t0).TotalMinutes, 1) + " minutes")
