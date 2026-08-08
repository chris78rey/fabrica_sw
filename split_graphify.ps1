$source = [IO.File]::ReadAllLines("inst.md")
$out = "docs/graphify"
$ranges = @(
    @{Name="01-contexto-arquitectura.md"; Start=1; End=20}
    @{Name="02-prompts-agentes.md"; Start=21; End=79}
    @{Name="03-blueprint-langgraph.md"; Start=80; End=188}
    @{Name="04-integracion-graphify.md"; Start=189; End=198}
    @{Name="05-safe-factory-tools.md"; Start=199; End=421}
    @{Name="06-developer-node.md"; Start=422; End=641}
    @{Name="07-safe-factory-app.md"; Start=642; End=992}
    @{Name="08-github-safe-pusher.md"; Start=993; End=1009}
    @{Name="09-simulacion-factory.md"; Start=1010; End=$source.Count}
)

foreach ($range in $ranges) {
    $content = $source[($range.Start - 1)..($range.End - 1)] -join [Environment]::NewLine
    [IO.File]::WriteAllText((Join-Path $out $range.Name), $content, [Text.UTF8Encoding]::new($false))
}

Write-Output "CREATED $($ranges.Count) files"
