$ErrorActionPreference = 'Stop'
$root = if ($args.Count -gt 0) { $args[0] } else { 'C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized' }
python (Join-Path $PSScriptRoot 'audit.py') --external-root $root
if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'DECIMAL_AUDIT=PASS_WITH_TRUE_DH_PENDING'
