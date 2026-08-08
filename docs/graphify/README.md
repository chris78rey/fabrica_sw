# Fábrica autónoma: corpus dividido para Graphify

Este corpus separa el diseño de `inst.md` por responsabilidad. El archivo original se conserva como referencia completa.

## Orden recomendado

1. `01-contexto-arquitectura.md` — reemplazo de Buzz y mapa de componentes.
2. `02-prompts-agentes.md` — contratos de Arquitecto, Desarrollador y Auditor.
3. `03-blueprint-langgraph.md` — estado, nodos, rutas y persistencia.
4. `04-integracion-graphify.md` — consultas, MCP, hooks y estrategia de tokens.
5. `05-safe-factory-tools.md` — herramientas de archivos, consola y Graphify.
6. `06-developer-node.md` — implementación del nodo desarrollador.
7. `07-safe-factory-app.md` — orquestación completa con LangGraph.
8. `08-github-safe-pusher.md` — commit y push controlados.
9. `09-simulacion-factory.md` — ejecución simulada de extremo a extremo.

Para generar el grafo de esta versión:

```text
graphify docs/graphify --mode deep --directed --wiki
```

La numeración ayuda a leer el flujo; las relaciones siguen estando explícitas en cada documento mediante nombres de módulos, funciones, herramientas y estados compartidos.

## Hook de sincronización

El hook versionable está en `.githooks/post-commit`. Para activarlo en un repositorio Git existente, ejecuta desde la raíz del proyecto:

```powershell
powershell.exe -NoProfile -File scripts\install-git-hooks.ps1
```

El hook ejecuta `graphify update <raíz> --code-only --no-cluster` después de cada commit y no bloquea el commit si la reconstrucción falla.
