# Graph Report - .  (2026-08-08)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 419 nodes · 782 edges · 34 communities (24 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- __init__.py
- FactoryStateContractTests
- safe_factory_tools.py
- ensure_commit_approved
- load_model_config
- architect_node
- auditor.py
- Plan de implementación de la fábrica segura
- github_secure_push_tool
- .test_auditor_ejecuta_herramienta_y_recibe_su_resultado
- test_workflow_cycle.py
- validate_password_complexity
- inst.md
- execute_test_command
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
1. `FactoryState` - 27 edges
2. `Plan de implementación de la fábrica segura` - 21 edges
3. `FactoryStateContractTests` - 20 edges
4. `create_initial_state()` - 18 edges
5. `architect_node()` - 17 edges
6. `auditor_node()` - 17 edges
7. `validate_safe_path()` - 17 edges
8. `developer_node()` - 16 edges
9. `build_autonomous_factory()` - 16 edges
10. `github_secure_push_tool()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `FactoryStateContractTests` --uses--> `ArchitectureBlueprint`  [INFERRED]
  tests/test_state.py → src/fabrica_sw/state.py
- `FactoryStateContractTests` --uses--> `FactoryState`  [INFERRED]
  tests/test_state.py → src/fabrica_sw/state.py
- `AuditorToolModel` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py
- `FakeModel` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py
- `FakeResponse` --uses--> `LocalAutonomousFactory`  [INFERRED]
  tests/test_workflow.py → src/fabrica_sw/workflow.py

## Import Cycles
- None detected.

## Communities (34 total, 10 thin omitted)

### Community 0 - "__init__.py"
Cohesion: 0.07
Nodes (41): auditor_should_continue_router(), Envía las llamadas del Auditor al ejecutor antes de aplicar la política., build_tool_executor_node(), _call_data(), developer_node(), LocalToolNode, _message_content(), Any (+33 more)

### Community 1 - "FactoryStateContractTests"
Cohesion: 0.06
Nodes (26): build_persistence_config(), build_thread_config(), open_checkpoint_saver(), Any, Path, Resuelve la base SQLite y crea solo su directorio padre., Construye la configuración que LangGraph usa para reanudar un hilo., Abre un ``SqliteSaver`` para compilar un grafo con checkpoints. (+18 more)

### Community 2 - "safe_factory_tools.py"
Cohesion: 0.08
Nodes (20): PathLike, graphify_query_tool(), graphify_shortest_path_tool(), list_directory_tool(), Herramientas de archivos restringidas al workspace de la fábrica., Consulta el grafo de conocimiento de Graphify sin cargar el código completo., Encuentra el camino más corto de dependencias entre dos símbolos., Lee un archivo de texto UTF-8 dentro del workspace seguro. (+12 more)

### Community 3 - "ensure_commit_approved"
Cohesion: 0.09
Nodes (18): _audit_and_measure_progress(), main(), Simulación local del flujo de la fábrica, sin commit ni push reales., _write_initial_files(), ensure_commit_approved(), Any, Políticas de autorización para operaciones Git de la fábrica., Permite continuar solo con una aprobación booleana explícita. La operación Git… (+10 more)

### Community 4 - "load_model_config"
Cohesion: 0.15
Nodes (19): RuntimeError, create_model(), _environment(), _load_chat_openai(), load_model_config(), ModelConfig, ModelConfigurationError, ModelFactoryError (+11 more)

### Community 5 - "architect_node"
Cohesion: 0.14
Nodes (14): architect_node(), _as_string_list(), _build_blueprint(), _extract_json_object(), Any, Nodo de arquitectura con consulta previa al grafo de Graphify., Extrae un objeto JSON aunque el modelo lo envuelva en markdown., Consulta Graphify y produce un blueprint arquitectónico estructurado. (+6 more)

### Community 6 - "auditor.py"
Cohesion: 0.13
Nodes (13): auditor_node(), _calculate_completion_percentage(), _extract_audit_decision(), Any, Nodo de auditoría segura para validar el trabajo del desarrollador., Extrae una decisión sin aprobar por accidente una respuesta ambigua., Lee el checklist conocido sin salir del workspace seguro., Audita el estado actual y devuelve aprobación, informe y avance. (+5 more)

### Community 7 - "Plan de implementación de la fábrica segura"
Cohesion: 0.09
Nodes (21): 0. Base del proyecto, 1. Arquitectura y estado persistente, 2. Herramientas de ejecución segura, 3. Flujo LangGraph seguro, 4. Sincronización Git y Graphify, 5. Validación y entrega, Criterio de avance, Cómo marcar el avance (+13 more)

### Community 8 - "github_secure_push_tool"
Cohesion: 0.21
Nodes (11): github_secure_push_tool(), _mask_token(), Any, Push seguro a GitHub después de una aprobación y un commit local., Crea un helper efímero que devuelve el token únicamente desde el entorno., Publica el commit actual en GitHub sin exponer el token en comandos o logs., _validate_ref(), _write_askpass_helper() (+3 more)

### Community 9 - ".test_auditor_ejecuta_herramienta_y_recibe_su_resultado"
Cohesion: 0.16
Nodes (5): AuditorToolModel, FakeModel, FakeResponse, ToolCallResponse, WorkflowConstructionTests

### Community 10 - "test_workflow_cycle.py"
Cohesion: 0.21
Nodes (5): AuditorModel, DeveloperModel, FakeResponse, run_cycle(), WorkflowCycleTests

### Community 11 - "validate_password_complexity"
Cohesion: 0.22
Nodes (6): hash_password_secure(), Controles reutilizables para credenciales., Genera un hash PBKDF2 con una sal aleatoria por contraseña., Valida longitud mínima, una mayúscula y un dígito., validate_password_complexity(), AuthSecurityTests

### Community 12 - "inst.md"
Cohesion: 0.17
Nodes (11): 1. Reemplazo de Componentes (De Buzz a Puro Python), 2. Prompts de Sistema para los Agentes en LangGraph, 3. Blueprint de Implementación en Python (LangGraph), 4. Conectando Graphify en Modo Autónomo y Bajo Consumo, Agente 1: El Arquitecto Contextual (`@Architect`), Agente 2: El Desarrollador de Software (`@Developer`), Agente 3: El Auditor de Seguridad e Integridad (`@Auditor`), Estructura técnica de `developer_node.py`: (+3 more)

### Community 13 - "execute_test_command"
Cohesion: 0.25
Nodes (5): execute_test_command(), _is_safe_command(), Permite perfiles de verificación, no intérpretes ni operaciones mutantes., Ejecuta un comando permitido sin shell y con timeout de 30 segundos., ExecuteTestCommandTests

### Community 14 - "2. Prompts de Sistema para los Agentes en LangGraph"
Cohesion: 0.40
Nodes (4): 2. Prompts de Sistema para los Agentes en LangGraph, Agente 1: El Arquitecto Contextual (`@Architect`), Agente 2: El Desarrollador de Software (`@Developer`), Agente 3: El Auditor de Seguridad e Integridad (`@Auditor`)

### Community 15 - "Persistencia, recuperación y límite de iteraciones"
Cohesion: 0.50
Nodes (3): Guardar y reanudar una ejecución, Persistencia, recuperación y límite de iteraciones, Política del flujo

### Community 16 - "Fábrica autónoma: corpus dividido para Graphify"
Cohesion: 0.50
Nodes (3): Fábrica autónoma: corpus dividido para Graphify, Hook de sincronización, Orden recomendado

### Community 17 - "Fábrica de Software Segura"
Cohesion: 0.50
Nodes (3): Desarrollo, Estado, Fábrica de Software Segura

## Knowledge Gaps
- **47 isolated node(s):** `fabrica-sw`, `Estado`, `Desarrollo`, `Cómo marcar el avance`, `0. Base del proyecto` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FactoryState` connect `__init__.py` to `FactoryStateContractTests`, `architect_node`, `auditor.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `github_secure_push_tool()` connect `github_secure_push_tool` to `__init__.py`, `FactoryStateContractTests`, `ensure_commit_approved`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `LocalAutonomousFactory` connect `__init__.py` to `.test_auditor_ejecuta_herramienta_y_recibe_su_resultado`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FactoryState` (e.g. with `LocalToolNode` and `LocalAutonomousFactory`) actually correct?**
  _`FactoryState` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `FactoryStateContractTests` (e.g. with `ArchitectureBlueprint` and `FactoryState`) actually correct?**
  _`FactoryStateContractTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fabrica-sw`, `Estado`, `Desarrollo` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07490079365079365 - nodes in this community are weakly interconnected._