# Graph Report - fabrica_sw  (2026-08-08)

## Corpus Check
- 59 files · ~27,563 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 464 nodes · 898 edges · 31 communities (21 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 59 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `61842af4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- auditor.py
- workflow.py
- create_initial_state
- AuditorTests
- load_model_config
- __init__.py
- architect.py
- Plan de implementación de la fábrica segura
- test_workflow_cycle.py
- LocalAutonomousFactory
- build_tasks
- simulate_factory_run.py
- inst.md
- 2. Prompts de Sistema para los Agentes en LangGraph
- Persistencia, recuperación y límite de iteraciones
- Fábrica autónoma: corpus dividido para Graphify
- Fábrica de Software Segura
- GraphifyHookTests
- execute_test_command
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
1. `FactoryState` - 31 edges
2. `create_initial_state()` - 22 edges
3. `Plan de implementación de la fábrica segura` - 21 edges
4. `build_autonomous_factory()` - 20 edges
5. `FactoryStateContractTests` - 20 edges
6. `architect_node()` - 17 edges
7. `auditor_node()` - 17 edges
8. `developer_node()` - 17 edges
9. `load_model_config()` - 17 edges
10. `validate_safe_path()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `FactoryStateContractTests` --uses--> `FactoryState`  [INFERRED]
  tests/test_state.py → src/fabrica_sw/state.py
- `main()` --calls--> `ensure_commit_approved()`  [EXTRACTED]
  simulate_factory_run.py → src/fabrica_sw/git_policy.py
- `run_cycle()` --calls--> `auditor_node()`  [EXTRACTED]
  tests/test_workflow_cycle.py → src/fabrica_sw/auditor.py
- `run_cycle()` --calls--> `developer_node()`  [EXTRACTED]
  tests/test_workflow_cycle.py → src/fabrica_sw/developer.py
- `DeveloperNodeTests` --uses--> `LocalToolNode`  [INFERRED]
  tests/test_developer.py → src/fabrica_sw/developer.py

## Import Cycles
- None detected.

## Communities (31 total, 10 thin omitted)

### Community 0 - "auditor.py"
Cohesion: 0.06
Nodes (31): ArgumentParser, PathLike, Nodo de auditoría segura para validar el trabajo del desarrollador., Lee el checklist conocido sin salir del workspace seguro., _read_checklist(), build_parser(), _configure_loaded_workspace(), main() (+23 more)

### Community 1 - "workflow.py"
Cohesion: 0.07
Nodes (48): auditor_node(), auditor_should_continue_router(), Any, Envía las llamadas del Auditor al ejecutor antes de aplicar la política., Audita el estado actual y devuelve aprobación, informe y avance., _response_content(), build_tool_executor_node(), _call_data() (+40 more)

### Community 2 - "create_initial_state"
Cohesion: 0.06
Nodes (30): RuntimeError, build_persistence_config(), build_thread_config(), open_checkpoint_saver(), Any, Path, Configuración de persistencia durable para la fábrica., Resuelve la base SQLite y crea solo su directorio padre. (+22 more)

### Community 3 - "AuditorTests"
Cohesion: 0.15
Nodes (6): _calculate_completion_percentage(), _extract_audit_decision(), Extrae una decisión sin aprobar por accidente una respuesta ambigua., AuditorTests, FakeModel, FakeResponse

### Community 4 - "load_model_config"
Cohesion: 0.13
Nodes (21): ModelRole, create_model(), create_models(), _environment(), _load_chat_openai(), load_model_config(), ModelConfig, ModelConfigurationError (+13 more)

### Community 5 - "__init__.py"
Cohesion: 0.07
Nodes (28): ensure_commit_approved(), Any, Políticas de autorización para operaciones Git de la fábrica., Permite continuar solo con una aprobación booleana explícita. La operación Git…, git_secure_commit_tool(), Any, Herramientas Git con selección explícita y autorización de auditoría., Valida y convierte rutas seleccionadas a rutas relativas al workspace. (+20 more)

### Community 6 - "architect.py"
Cohesion: 0.14
Nodes (16): architect_node(), _as_string_list(), _build_blueprint(), _extract_json_object(), _infer_impacted_files(), Any, Nodo de arquitectura con consulta previa al grafo de Graphify., Extrae un objeto JSON aunque el modelo lo envuelva en markdown. (+8 more)

### Community 7 - "Plan de implementación de la fábrica segura"
Cohesion: 0.09
Nodes (21): 0. Base del proyecto, 1. Arquitectura y estado persistente, 2. Herramientas de ejecución segura, 3. Flujo LangGraph seguro, 4. Sincronización Git y Graphify, 5. Validación y entrega, Criterio de avance, Cómo marcar el avance (+13 more)

### Community 8 - "test_workflow_cycle.py"
Cohesion: 0.21
Nodes (5): AuditorModel, DeveloperModel, FakeResponse, run_cycle(), WorkflowCycleTests

### Community 9 - "LocalAutonomousFactory"
Cohesion: 0.11
Nodes (14): detect_test_command(), Path, Detección conservadora de comandos de verificación por tipo de proyecto., Devuelve un comando seguro y portable para el proyecto detectado. La detección…, Resuelve ejecutables, permitiendo configurar Godot fuera del PATH., resolve_test_executable(), LocalAutonomousFactory, Ejecutor determinista del flujo cuando LangGraph no está disponible. (+6 more)

### Community 10 - "build_tasks"
Cohesion: 0.27
Nodes (5): build_tasks(), Any, Conversión pequeña y determinista de requisitos en tareas trazables., Extrae checklists o pasos numerados; si no existen, crea una tarea., TaskPlannerTests

### Community 11 - "simulate_factory_run.py"
Cohesion: 0.13
Nodes (11): _audit_and_measure_progress(), main(), Simulación local del flujo de la fábrica, sin commit ni push reales., _write_initial_files(), hash_password_secure(), Controles reutilizables para credenciales., Genera un hash PBKDF2 con una sal aleatoria por contraseña., Valida longitud mínima, una mayúscula y un dígito. (+3 more)

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

### Community 18 - "execute_test_command"
Cohesion: 0.25
Nodes (5): execute_test_command(), _is_safe_command(), Permite perfiles de verificación, no intérpretes ni operaciones mutantes., Ejecuta un comando permitido sin shell y con timeout de 30 segundos., ExecuteTestCommandTests

## Knowledge Gaps
- **47 isolated node(s):** `fabrica-sw`, `Estado`, `Desarrollo`, `Cómo marcar el avance`, `0. Base del proyecto` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_initial_state()` connect `create_initial_state` to `auditor.py`, `workflow.py`, `AuditorTests`, `__init__.py`, `test_workflow_cycle.py`, `LocalAutonomousFactory`, `build_tasks`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `FactoryState` connect `workflow.py` to `auditor.py`, `create_initial_state`, `__init__.py`, `architect.py`, `LocalAutonomousFactory`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FactoryState` (e.g. with `LocalToolNode` and `LocalAutonomousFactory`) actually correct?**
  _`FactoryState` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `build_autonomous_factory()` (e.g. with `should_continue_router()` and `_apply_quality_gate()`) actually correct?**
  _`build_autonomous_factory()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `FactoryStateContractTests` (e.g. with `ArchitectureBlueprint` and `FactoryState`) actually correct?**
  _`FactoryStateContractTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fabrica-sw`, `Estado`, `Desarrollo` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `auditor.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05786090005844535 - nodes in this community are weakly interconnected._