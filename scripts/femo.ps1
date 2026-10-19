# Launcher Windows: usa Python existente, sem mudar PATH ou instalar software.
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$FemoArguments)
$ErrorActionPreference = 'Stop'
$FemoPython = $null
$FemoCandidates = @(
    (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'),
    (Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')
)
foreach ($FemoCandidate in $FemoCandidates) {
    if (Test-Path -LiteralPath $FemoCandidate -PathType Leaf) { $FemoPython = $FemoCandidate; break }
}
if (-not $FemoPython) {
    $FemoCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($FemoCommand -and $FemoCommand.Source -notlike '*WindowsApps*') { $FemoPython = $FemoCommand.Source }
}
if (-not $FemoPython) { throw 'Python 3.10+ não localizado. Instale pelo site oficial ou informe seu interpretador à IA.' }
& $FemoPython -X utf8 (Join-Path $PSScriptRoot 'femo.py') @FemoArguments
exit $LASTEXITCODE
