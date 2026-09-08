param(
  [Parameter(Mandatory=$true)][string]$CandidateDirectory,
  [Parameter(Mandatory=$true)][string]$MathlibDirectory,
  [Parameter(Mandatory=$true)][string]$LeanSourceDirectory,
  [switch]$Compact
)
$ErrorActionPreference = 'Stop'
# Read-only static source inventory. No Lean/Lake execution and no file writes.
$packetRoots = @([pscustomobject]@{label='overlay';path=(Resolve-Path -LiteralPath $CandidateDirectory).Path},
  [pscustomobject]@{label='mathlib';path=(Resolve-Path -LiteralPath $MathlibDirectory).Path},
  [pscustomobject]@{label='lean';path=(Resolve-Path -LiteralPath $LeanSourceDirectory).Path})
$packetLockPath = Join-Path $MathlibDirectory 'lake-manifest.json'
$packetLock = Get-Content -LiteralPath $packetLockPath -Raw | ConvertFrom-Json
foreach ($packetPkg in $packetLock.packages) {
  $packetPkgPath = Join-Path $MathlibDirectory ".lake/packages/$($packetPkg.name)"
  if (Test-Path -LiteralPath $packetPkgPath) {
    $packetRoots += [pscustomobject]@{label="package:$($packetPkg.name)";path=(Resolve-Path -LiteralPath $packetPkgPath).Path}
  }
}
$packetQueue = [System.Collections.Generic.Queue[string]]::new()
$packetQueue.Enqueue('NEW_QUOTIENT_CLM_API_Probe20260908')
$packetSeen = @{}
$packetModules = [System.Collections.Generic.List[object]]::new()
$packetMissing = [System.Collections.Generic.List[string]]::new()
$packetAmbiguous = [System.Collections.Generic.List[object]]::new()
$packetUnparsed = [System.Collections.Generic.List[object]]::new()
while ($packetQueue.Count -gt 0) {
  $packetName = $packetQueue.Dequeue()
  if ($packetSeen.ContainsKey($packetName)) { continue }
  $packetSeen[$packetName] = $true
  $packetRelative = $packetName.Replace('.', '/') + '.lean'
  $packetMatches = @()
  foreach ($packetRoot in $packetRoots) {
    $packetFile = Join-Path $packetRoot.path $packetRelative
    if (Test-Path -LiteralPath $packetFile -PathType Leaf) {
      $packetMatches += [pscustomobject]@{root=$packetRoot.label;path=$packetFile}
    }
  }
  if ($packetMatches.Count -eq 0) { $packetMissing.Add($packetName); continue }
  if ($packetMatches.Count -gt 1) {
    $packetAmbiguous.Add([pscustomobject]@{module=$packetName;matches=$packetMatches})
    continue
  }
  $packetMatch = $packetMatches[0]
  $packetRaw = Get-Content -LiteralPath $packetMatch.path -Raw
  # Remove nested block comments from the inside out, then line comments.
  # This is a lexical inventory, not a Lean parser or elaborator.
  $packetClean = $packetRaw
  do {
    $packetPrior = $packetClean
    $packetClean = [regex]::Replace($packetClean, '(?s)/-(?:(?!/-|-/).)*-/', ' ')
  } while ($packetPrior -cne $packetClean)
  $packetClean = [regex]::Replace($packetClean, '(?m)--[^\r\n]*', '')
  $packetImports = [System.Collections.Generic.List[string]]::new()
  if ($packetClean -notmatch '(?m)^\s*prelude\s*$') { $packetImports.Add('Init') }
  foreach ($packetLine in ($packetClean -split '\r?\n')) {
    if ($packetLine -match '^\s*(?:module|prelude)?\s*$') { continue }
    if ($packetLine -match '^\s*(?:(?:public|private|meta)\s+)*import\s+(.+?)\s*$') {
      $packetRest = $Matches[1] -replace '^all\s+', ''
      foreach ($packetToken in ($packetRest -split '\s+')) {
        if ($packetToken -match '^[A-Za-z_][A-Za-z0-9_\x27]*(\.[A-Za-z_][A-Za-z0-9_\x27]*)*$') {
          $packetImports.Add($packetToken)
        } else { $packetUnparsed.Add([pscustomobject]@{module=$packetName;line=$packetLine}) }
      }
    } else { break } # Imports are in the header; exclude JS imports inside later widget strings.
  }
  $packetDeps = @($packetImports | Sort-Object -Unique)
  foreach ($packetDep in $packetDeps) { $packetQueue.Enqueue($packetDep) }
  $packetModules.Add([pscustomobject]@{module=$packetName;root=$packetMatch.root;
    relative_path=$packetRelative;sha256=(Get-FileHash -LiteralPath $packetMatch.path -Algorithm SHA256).Hash.ToLowerInvariant();imports=$packetDeps})
}
$packetResult = [pscustomobject]@{
  schema='quotient-clm-static-import-inventory-v1';execution='STATIC_ONLY_NOT_LEAN';
  lexical_parser_limit='Regex comment removal; not a Lean header parser. Runner must reconcile against actual compiler imports.';
  module_count=$packetModules.Count;missing=@($packetMissing);ambiguous=@($packetAmbiguous);unparsed=@($packetUnparsed);
  mathlib_lock_sha256=(Get-FileHash -LiteralPath $packetLockPath).Hash.ToLowerInvariant();
  dependency_lock=$packetLock;modules=@($packetModules | Sort-Object module)
}
if ($Compact) {
  $packetGraphJson = $packetResult | ConvertTo-Json -Depth 30 -Compress
  $packetDigest = [System.Security.Cryptography.SHA256]::HashData([System.Text.Encoding]::UTF8.GetBytes($packetGraphJson))
  [pscustomobject]@{schema='quotient-clm-static-import-index-v1';module_count=$packetModules.Count;
    graph_utf8_sha256=[Convert]::ToHexString($packetDigest).ToLowerInvariant();
    missing=@($packetMissing);ambiguous=@($packetAmbiguous);unparsed=@($packetUnparsed);
    mathlib_lock_sha256=$packetResult.mathlib_lock_sha256;dependency_lock=$packetLock;
    modules=@($packetModules | Sort-Object module | ForEach-Object { "$($_.root)|$($_.module)|$($_.sha256)" })
  } | ConvertTo-Json -Depth 30 -Compress
} else { $packetResult | ConvertTo-Json -Depth 30 -Compress }
