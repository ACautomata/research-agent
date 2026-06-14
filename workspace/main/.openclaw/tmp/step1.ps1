$env:PYTHONUTF8 = '1'
$env:MAX_QAS = '1'
$env:BENCH_MODEL = 'deepseek/deepseek-v4-flash'
$base = 'D:\Code\= =\research-agent'
python (Join-Path $base 'workspace\bench_prepare.py')
