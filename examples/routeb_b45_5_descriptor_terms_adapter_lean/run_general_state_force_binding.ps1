Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$side = $PSScriptRoot
$exporter = Join-Path $side 'general_state_force_binding_export.jl'
$verifier = Join-Path $side 'verify_general_state_force_binding.py'
$out = Join-Path $side 'output/general-state-export-20260907'
$source = Join-Path (Split-Path (Split-Path (Split-Path $side -Parent) -Parent) -Parent) '6dof_sos_optimized/6dof_sos_optimized/robot_final/dhport_lib.jl'
$expectedExporter = '5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4'
$expectedSource = 'aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936'

if (-not (Get-Command julia -ErrorAction SilentlyContinue)) {
    Write-Output 'PENDING_JULIA_EXECUTION=JULIA_NOT_FOUND'
    exit 2
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Output 'PENDING_JULIA_EXECUTION=PYTHON_NOT_FOUND'
    exit 2
}
if (-not (Test-Path -LiteralPath $exporter) -or -not (Test-Path -LiteralPath $verifier) -or -not (Test-Path -LiteralPath $source)) {
    Write-Output 'REJECTED_INPUT=REQUIRED_FILE_MISSING'
    exit 3
}

$actualExporter = (Get-FileHash -Algorithm SHA256 -LiteralPath $exporter).Hash.ToLowerInvariant()
$actualSource = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLowerInvariant()
if ($actualExporter -ne $expectedExporter) {
    Write-Output "REJECTED_INPUT=EXPORTER_HASH_DRIFT:$actualExporter"
    exit 3
}
if ($actualSource -ne $expectedSource) {
    Write-Output "REJECTED_INPUT=DEPLOYED_SOURCE_HASH_DRIFT:$actualSource"
    exit 3
}
if (Test-Path -LiteralPath $out) {
    Write-Output "PENDING_FRESH_OUTPUT_DIR_EXISTS=$out"
    exit 2
}

New-Item -ItemType Directory -Force -Path $out | Out-Null
$stdout = Join-Path $out 'worker.stdout.txt'
$stderr = Join-Path $out 'worker.stderr.txt'
$exitFile = Join-Path $out 'worker.exit-code.txt'

& julia --startup-file=no $exporter 1> $stdout 2> $stderr
$exitCode = $LASTEXITCODE
$exitCode | Set-Content -NoNewline -Encoding utf8 $exitFile

& python $verifier --export-dir $out --stdout $stdout --stderr $stderr --exit-code $exitFile
exit $LASTEXITCODE
