# Graph Report - fabrica_sw  (2026-08-08)

## Corpus Check
- 59 files · ~27,113 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 459 nodes · 878 edges · 30 communities (20 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 58 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `61842af4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- safe_factory_tools.py
- workflow.py
- create_initial_state
- auditor.py
- __init__.py
- ensure_commit_approved
- architect.py
- Plan de implementación de la fábrica segura
- github_secure_push_tool
- test_workflow.py
- cli.py
- validate_password_complexity
- inst.md
- 2. Prompts de Sistema para los Agentes en LangGraph
- Persistencia, recuperación y límite de iteraciones
- Fábrica autónoma: corpus dividido para Graphify
- Fábrica de Software Segura
- GraphifyHookTests
- 01-contexto-arquitectura.md
- 03-blueprint-langgraph.md
- 04-integracion-graphify.md
- 05-safe-factory-tools.md
- 06-developer-node.md
- 07-safe-factory-app.md
- 09-simulacion-factory.md
- post-commit
- fabrica-sw

## God Nodes (most connected - your core abstractions)
1. `FactoryState` - 28 edges
2. `Plan de implementación de la fábrica segura` - 21 edges
3. `create_initial_state()` - 20 edges
4. `FactoryStateContractTests` - 20 edges
5. `build_autonomous_factory()` - 18 edges
6. `architect_node()` - 17 edges
7. `auditor_node()` - 17 edges
8. `developer_node()` - 17 edges
9. `load_model_config()` - 17 edges
10. `validate_safe_path()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `FactoryStateContractTests` --uses--> `FactoryState`  [INFERRED]
  tests/test_state.py → src/fabrica_sw/state.py
- `AuditorToolModel` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py
- `FakeModel` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py
- `FakeResponse` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py
- `ToolCallResponse` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py

## Import Cycles
- None detected.

## Communities (30 total, 10 thin omitted)

### Community 0 - "safe_factory_tools.py"
Cohesion: 0.06
Nodes (25): PathLike, execute_test_command(), graphify_query_tool(), graphify_shortest_path_tool(), _is_safe_command(), list_directory_tool(), Herramientas de archivos restringidas al workspace de la fábrica., Consulta el grafo de conocimiento de Graphify sin cargar el código completo. (+17 more)

### Community 1 - "workflow.py"
Cohesion: 0.08
Nodes (42): auditor_should_continue_router(), Envía las llamadas del Auditor al ejecutor antes de aplicar la política., build_tool_executor_node(), _call_data(), developer_node(), LocalToolNode, _message_content(), Any (+34 more)

### Community 2 - "create_initial_state"
Cohesion: 0.06
Nodes (33): RuntimeError, build_persistence_config(), build_thread_config(), open_checkpoint_saver(), Any, Path, Configuración de persistencia durable para la fábrica., Resuelve la base SQLite y crea solo su directorio padre. (+25 more)

### Community 3 - "auditor.py"
Cohesion: 0.08
Nodes (18): auditor_node(), _calculate_completion_percentage(), _extract_audit_decision(), Any, Nodo de auditoría segura para validar el trabajo del desarrollador., Extrae una decisión sin aprobar por accidente una respuesta ambigua., Lee el checklist conocido sin salir del workspace seguro., Audita el estado actual y devuelve aprobación, informe y avance. (+10 more)

### Community 4 - "__init__.py"
Cohesion: 0.13
Nodes (22): ModelRole, Componentes compartidos de la fábrica de software., create_model(), create_models(), _environment(), _load_chat_openai(), load_model_config(), ModelConfig (+14 more)

### Community 5 - "ensure_commit_approved"
Cohesion: 0.09
Nodes (18): _audit_and_measure_progress(), main(), Simulación local del flujo de la fábrica, sin commit ni push reales., _write_initial_files(), ensure_commit_approved(), Any, Políticas de autorización para operaciones Git de la fábrica., Permite continuar solo con una aprobación booleana explícita. La operación Git… (+10 more)

### Community 6 - "architect.py"
Cohesion: 0.14
Nodes (16): architect_node(), _as_string_list(), _build_blueprint(), _extract_json_object(), _infer_impacted_files(), Any, Nodo de arquitectura con consulta previa al grafo de Graphify., Extrae un objeto JSON aunque el modelo lo envuelva en markdown. (+8 more)

### Community 7 - "Plan de implementación de la fábrica segura"
Cohesion: 0.09
Nodes (21): 0. Base del proyecto, 1. Arquitectura y estado persistente, 2. Herramientas de ejecución segura, 3. Flujo LangGraph seguro, 4. Sincronización Git y Graphify, 5. Validación y entrega, Criterio de avance, Cómo marcar el avance (+13 more)

### Community 8 - "github_secure_push_tool"
Cohesion: 0.21
Nodes (11): github_secure_push_tool(), _mask_token(), Any, Push seguro a GitHub después de una aprobación y un commit local., Crea un helper efímero que devuelve el token únicamente desde el entorno., Publica el commit actual en GitHub sin exponer el token en comandos o logs., _validate_ref(), _write_askpass_helper() (+3 more)

### Community 9 - "test_workflow.py"
Cohesion: 0.10
Nodes (12): detect_test_command(), Path, Detección conservadora de comandos de verificación por tipo de proyecto., Devuelve un comando seguro y portable para el proyecto detectado. La detección…, Resuelve ejecutables, permitiendo configurar Godot fuera del PATH., resolve_test_executable(), TestProfileDetectionTests, AuditorToolModel (+4 more)

### Community 10 - "cli.py"
Cohesion: 0.13
Nodes (13): ArgumentParser, build_parser(), _configure_loaded_workspace(), main(), Path, Punto de entrada para ejecutar la fábrica sobre un repositorio local., Sincroniza las constantes importadas antes de procesar ``--repository``., build_tasks() (+5 more)

### Community 11 - "validate_password_complexity"
Cohesion: 0.22
Nodes (6): hash_password_secure(), Controles reutilizables para credenciales., Genera un hash PBKDF2 con una sal aleatoria por contraseña., Valida longitud mínima, una mayúscula y un dígito., validate_password_complexity(), AuthSecurityTests

### Community 12 - "inst.md"
Cohesion: 0.17
Nodes (11): 1. Reemplazo de Componentes (De Buzz a Puro Python), 2. Prompts de Sistema para los Agentes en LangGraph, 3. Blueprint de Implementación en Python (LangGraph), 4. Conectando Graphify en Modo Autónomo y Bajo Consumo, Agente 1: El Arquitecto Contextual (`@Architect`), Agente 2: El Desarrollador de Software (`@Developer`), Agente 3: El Auditor de Seguridad e Integridad (`@Auditor`), Estructura técnica de `developer_node.py`: (+3 more)

### Community 13 - "2. Prompts de Sistema para los Agentes en LangGraph"
Cohesion: 0.40
Nodes (4): 2. Prompts de Sistema para los Agentes en LangGraph, Agente 1: El Arquitecto Contextual (`@Architect`), Agente 2: El Desarrollador de Software (`@Developer`), Agente 3: El Auditor de Seguridad e Integridad (`@Auditor`)

### Community 14 - "Persistencia, recuperación y límite de iteraciones"
Cohesion: 0.50
Nodes (3): Guardar y reanudar una ejecución, Persistencia, recuperación y límite de iteraciones, Política del flujo

### Community 15 - "Fábrica autónoma: corpus dividido para Graphify"
Cohesion: 0.50
Nodes (3): Fábrica autónoma: corpus dividido para Graphify, Hook de sincronización, Orden recomendado

### Community 16 - "Fábrica de Software Segura"
Cohesion: 0.50
Nodes (3): Desarrollo, Estado, Fábrica de Software Segura

## Knowledge Gaps
- **47 isolated node(s):** `fabrica-sw`, `Estado`, `Desarrollo`, `Cómo marcar el avance`, `0. Base del proyecto` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_initial_state()` connect `create_initial_state` to `workflow.py`, `auditor.py`, `__init__.py`, `test_workflow.py`, `cli.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `FactoryState` connect `workflow.py` to `create_initial_state`, `auditor.py`, `__init__.py`, `architect.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `github_secure_push_tool()` connect `github_secure_push_tool` to `create_initial_state`, `__init__.py`, `ensure_commit_approved`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FactoryState` (e.g. with `LocalToolNode` and `LocalAutonomousFactory`) actually correct?**
  _`FactoryState` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `FactoryStateContractTests` (e.g. with `ArchitectureBlueprint` and `FactoryState`) actually correct?**
  _`FactoryStateContractTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `build_autonomous_factory()` (e.g. with `should_continue_router()` and `_apply_quality_gate()`) actually correct?**
  _`build_autonomous_factory()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fabrica-sw`, `Estado`, `Desarrollo` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._