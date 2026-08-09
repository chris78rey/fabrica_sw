# Graph Report - fabrica_sw  (2026-08-08)

## Corpus Check
- 67 files · ~30,318 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 534 nodes · 1055 edges · 33 communities (23 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6d35b6d6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- safe_factory_tools.py
- developer.py
- FactoryStateContractTests
- auditor.py
- __init__.py
- github_secure_push_tool
- architect.py
- Plan de implementación de la fábrica segura
- test_workflow_cycle.py
- create_initial_state
- runner.py
- validate_password_complexity
- inst.md
- 2. Prompts de Sistema para los Agentes en LangGraph
- Persistencia, recuperación y límite de iteraciones
- Fábrica autónoma: corpus dividido para Graphify
- Fábrica de Software Segura
- GraphifyHookTests
- workflow.py
- git_secure_commit_tool
- Interfaz local
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
2. `run_factory()` - 25 edges
3. `create_initial_state()` - 22 edges
4. `Plan de implementación de la fábrica segura` - 21 edges
5. `validate_safe_path()` - 20 edges
6. `build_autonomous_factory()` - 20 edges
7. `FactoryStateContractTests` - 20 edges
8. `architect_node()` - 17 edges
9. `auditor_node()` - 17 edges
10. `developer_node()` - 17 edges

## Surprising Connections (you probably didn't know these)
- `FactoryStateContractTests` --uses--> `FactoryState`  [INFERRED]
  tests/test_state.py → src/fabrica_sw/state.py
- `run_cycle()` --calls--> `auditor_node()`  [EXTRACTED]
  tests/test_workflow_cycle.py → src/fabrica_sw/auditor.py
- `run_cycle()` --calls--> `developer_node()`  [EXTRACTED]
  tests/test_workflow_cycle.py → src/fabrica_sw/developer.py
- `DeveloperNodeTests` --uses--> `LocalToolNode`  [INFERRED]
  tests/test_developer.py → src/fabrica_sw/developer.py
- `FakeModel` --uses--> `LocalToolNode`  [INFERRED]
  tests/test_developer.py → src/fabrica_sw/developer.py

## Import Cycles
- 3-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/architect.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 3-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 3-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 3-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 3-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/architect.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 4-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 5-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 5-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/architect.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 5-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 5-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/runner.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`
- 5-file cycle: `src/fabrica_sw/__init__.py -> src/fabrica_sw/workflow.py -> src/fabrica_sw/auditor.py -> src/fabrica_sw/developer.py -> src/fabrica_sw/safe_factory_tools.py -> src/fabrica_sw/__init__.py`

## Communities (33 total, 10 thin omitted)

### Community 0 - "safe_factory_tools.py"
Cohesion: 0.06
Nodes (29): PathLike, backup_before_write(), Path, Guarda una sola copia del archivo antes de su primera modificación., execute_test_command(), graphify_query_tool(), graphify_shortest_path_tool(), _is_safe_command() (+21 more)

### Community 1 - "developer.py"
Cohesion: 0.12
Nodes (16): build_tool_executor_node(), _call_data(), developer_node(), LocalToolNode, _message_content(), Any, Nodo de desarrollo y despacho seguro de llamadas a herramientas., Fallback compatible con ``langgraph.prebuilt.ToolNode`` para este venv. (+8 more)

### Community 2 - "FactoryStateContractTests"
Cohesion: 0.07
Nodes (22): RuntimeError, build_persistence_config(), build_thread_config(), open_checkpoint_saver(), Any, Path, Configuración de persistencia durable para la fábrica., Resuelve la base SQLite y crea solo su directorio padre. (+14 more)

### Community 3 - "auditor.py"
Cohesion: 0.13
Nodes (13): auditor_node(), _calculate_completion_percentage(), _extract_audit_decision(), Any, Nodo de auditoría segura para validar el trabajo del desarrollador., Extrae una decisión sin aprobar por accidente una respuesta ambigua., Lee el checklist conocido sin salir del workspace seguro., Audita el estado actual y devuelve aprobación, informe y avance. (+5 more)

### Community 4 - "__init__.py"
Cohesion: 0.13
Nodes (22): ModelRole, Componentes compartidos de la fábrica de software., create_model(), create_models(), _environment(), _load_chat_openai(), load_model_config(), ModelConfig (+14 more)

### Community 5 - "github_secure_push_tool"
Cohesion: 0.14
Nodes (14): github_secure_push_tool(), _mask_token(), Any, Push seguro a GitHub después de una aprobación y un commit local., Crea un helper efímero que devuelve el token únicamente desde el entorno., Publica el commit actual en GitHub sin exponer el token en comandos o logs., _validate_ref(), _write_askpass_helper() (+6 more)

### Community 6 - "architect.py"
Cohesion: 0.14
Nodes (16): architect_node(), _as_string_list(), _build_blueprint(), _extract_json_object(), _infer_impacted_files(), Any, Nodo de arquitectura con consulta previa al grafo de Graphify., Extrae un objeto JSON aunque el modelo lo envuelva en markdown. (+8 more)

### Community 7 - "Plan de implementación de la fábrica segura"
Cohesion: 0.09
Nodes (21): 0. Base del proyecto, 1. Arquitectura y estado persistente, 2. Herramientas de ejecución segura, 3. Flujo LangGraph seguro, 4. Sincronización Git y Graphify, 5. Validación y entrega, Criterio de avance, Cómo marcar el avance (+13 more)

### Community 8 - "test_workflow_cycle.py"
Cohesion: 0.21
Nodes (5): AuditorModel, DeveloperModel, FakeResponse, run_cycle(), WorkflowCycleTests

### Community 9 - "create_initial_state"
Cohesion: 0.08
Nodes (20): add_messages(), create_initial_state(), Any, Contratos de estado compartidos por el flujo Graphify/LangGraph., Valida la forma y los límites del estado completo. Los nodos pueden seguir…, Combina mensajes sin mutar las secuencias de entrada., Crea un estado completo y seguro para iniciar una ejecución., validate_factory_state() (+12 more)

### Community 10 - "runner.py"
Cohesion: 0.06
Nodes (54): ArgumentParser, AutonomyMode, AutonomyConfig, _env_bool(), Configuración de autonomía con límites explícitos y seguros., Límites de una ejecución de la fábrica. La instalación solo puede ocurrir…, build_parser(), main() (+46 more)

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

### Community 18 - "workflow.py"
Cohesion: 0.08
Nodes (41): auditor_should_continue_router(), Envía las llamadas del Auditor al ejecutor antes de aplicar la política., Envía llamadas de herramientas al ejecutor o termina la fase de desarrollo., should_continue_router(), FactoryState, Estado canónico compartido por arquitectura, desarrollo y auditoría., detect_test_command(), Path (+33 more)

### Community 19 - "git_secure_commit_tool"
Cohesion: 0.09
Nodes (18): _audit_and_measure_progress(), main(), Simulación local del flujo de la fábrica, sin commit ni push reales., _write_initial_files(), ensure_commit_approved(), Any, Políticas de autorización para operaciones Git de la fábrica., Permite continuar solo con una aprobación booleana explícita. La operación Git… (+10 more)

### Community 20 - "Interfaz local"
Cohesion: 0.40
Nodes (4): Arranque, Instalación, Interfaz local, Uso

## Knowledge Gaps
- **50 isolated node(s):** `fabrica-sw`, `Estado`, `Desarrollo`, `Instalación`, `Arranque` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_factory()` connect `runner.py` to `developer.py`, `__init__.py`, `create_initial_state`, `workflow.py`, `git_secure_commit_tool`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `create_initial_state()` connect `create_initial_state` to `developer.py`, `FactoryStateContractTests`, `auditor.py`, `__init__.py`, `github_secure_push_tool`, `test_workflow_cycle.py`, `runner.py`, `workflow.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `FactoryState` connect `workflow.py` to `developer.py`, `FactoryStateContractTests`, `auditor.py`, `__init__.py`, `architect.py`, `create_initial_state`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FactoryState` (e.g. with `LocalToolNode` and `LocalAutonomousFactory`) actually correct?**
  _`FactoryState` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fabrica-sw`, `Estado`, `Desarrollo` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `safe_factory_tools.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05727644652250146 - nodes in this community are weakly interconnected._
- **Should `developer.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12183908045977011 - nodes in this community are weakly interconnected._