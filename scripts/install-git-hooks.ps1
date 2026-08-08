param(
    [string]$Repository = (Get-Location).Path
)

$resolvedRepository = (Resolve-Path -LiteralPath $Repository).Path
$gitDirectory = Join-Path $resolvedRepository ".git"
if (-not (Test-Path -LiteralPath $gitDirectory -PathType Container)) {
    throw "No existe un repositorio Git en '$resolvedRepository'."
}

git -C $resolvedRepository config core.hooksPath .githooks
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo configurar core.hooksPath."
}

Write-Output "Hook Graphify configurado: $resolvedRepository\.githooks"
