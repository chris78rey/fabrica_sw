# Graph Report - fabrica_sw  (2026-08-08)

## Corpus Check
- 67 files · ~30,837 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 537 nodes · 1062 edges · 43 communities (32 shown, 11 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d2446a25`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- validate_safe_path
- __init__.py
- FactoryStateContractTests
- AuditorTests
- load_model_config
- github_secure_push_tool
- architect.py
- Plan de implementación de la fábrica segura
- test_workflow_cycle.py
- test_workflow.py
- runner.py
- validate_password_complexity
- inst.md
- 2. Prompts de Sistema para los Agentes en LangGraph
- Persistencia, recuperación y límite de iteraciones
- Fábrica autónoma: corpus dividido para Graphify
- Fábrica de Software Segura
- GraphifyHookTests
- persistence.py
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
- create_initial_state
- FactoryRunRequest
- safe_factory_tools.py
- execute_test_command
- build_tasks
- AutonomyConfig
- dependency_tools.py
- ui_streamlit.py
- build_thread_config
- ArchitectureBlueprint

## God Nodes (most connected - your core abstractions)
1. `FactoryState` - 33 edges
2. `run_factory()` - 26 edges
3. `create_initial_state()` - 22 edges
4. `Plan de implementación de la fábrica segura` - 21 edges
5. `validate_safe_path()` - 20 edges
6. `FactoryStateContractTests` - 20 edges
7. `architect_node()` - 17 edges
8. `auditor_node()` - 17 edges
9. `developer_node()` - 17 edges
10. `load_model_config()` - 17 edges

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

## Communities (43 total, 11 thin omitted)

### Community 0 - "validate_safe_path"
Cohesion: 0.11
Nodes (14): PathLike, list_directory_tool(), Lista, ordenados, los archivos y carpetas de un directorio seguro., Lee un archivo de texto UTF-8 dentro del workspace seguro., Escribe de forma atómica, reversible y no destructiva., read_file_tool(), write_file_tool(), Path (+6 more)

### Community 1 - "__init__.py"
Cohesion: 0.06
Nodes (61): auditor_node(), auditor_should_continue_router(), _calculate_completion_percentage(), Any, Nodo de auditoría segura para validar el trabajo del desarrollador., Envía las llamadas del Auditor al ejecutor antes de aplicar la política., Lee el checklist conocido sin salir del workspace seguro., Audita el estado actual y devuelve aprobación, informe y avance. (+53 more)

### Community 2 - "FactoryStateContractTests"
Cohesion: 0.17
Nodes (7): evaluate_workflow_route(), evaluate_workflow_router(), Any, Políticas deterministas para el ciclo Desarrollador--Auditor., Decide corrección, despliegue o detención con un límite seguro., Alias de compatibilidad para el nombre usado en la primera versión., FactoryStateContractTests

### Community 3 - "AuditorTests"
Cohesion: 0.16
Nodes (5): _extract_audit_decision(), Extrae una decisión sin aprobar por accidente una respuesta ambigua., AuditorTests, FakeModel, FakeResponse

### Community 4 - "load_model_config"
Cohesion: 0.13
Nodes (19): ModelRole, create_model(), _environment(), _load_chat_openai(), load_model_config(), ModelConfig, ModelConfigurationError, ModelFactoryError (+11 more)

### Community 5 - "github_secure_push_tool"
Cohesion: 0.14
Nodes (14): github_secure_push_tool(), _mask_token(), Any, Push seguro a GitHub después de una aprobación y un commit local., Crea un helper efímero que devuelve el token únicamente desde el entorno., Publica el commit actual en GitHub sin exponer el token en comandos o logs., _validate_ref(), _write_askpass_helper() (+6 more)

### Community 6 - "architect.py"
Cohesion: 0.09
Nodes (21): architect_node(), _as_string_list(), _build_blueprint(), _extract_json_object(), _infer_impacted_files(), Any, Nodo de arquitectura con consulta previa al grafo de Graphify., Extrae un objeto JSON aunque el modelo lo envuelva en markdown. (+13 more)

### Community 7 - "Plan de implementación de la fábrica segura"
Cohesion: 0.09
Nodes (21): 0. Base del proyecto, 1. Arquitectura y estado persistente, 2. Herramientas de ejecución segura, 3. Flujo LangGraph seguro, 4. Sincronización Git y Graphify, 5. Validación y entrega, Criterio de avance, Cómo marcar el avance (+13 more)

### Community 8 - "test_workflow_cycle.py"
Cohesion: 0.21
Nodes (5): AuditorModel, DeveloperModel, FakeResponse, run_cycle(), WorkflowCycleTests

### Community 9 - "test_workflow.py"
Cohesion: 0.09
Nodes (15): detect_test_command(), Path, Detección conservadora de comandos de verificación por tipo de proyecto., Devuelve un comando seguro y portable para el proyecto detectado. La detección…, Resuelve ejecutables, permitiendo configurar Godot fuera del PATH., Valida un proyecto HTML/JavaScript sin requerir un runner externo., resolve_test_executable(), validate_static_web_project() (+7 more)

### Community 10 - "runner.py"
Cohesion: 0.13
Nodes (23): get_last_dependency_result(), ensure_git_repository(), Path, Inicializa Git solo si el workspace aún no es un repositorio., create_models(), Construye un modelo independiente para cada rol de la fábrica., _build_report(), configure_loaded_workspace() (+15 more)

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

### Community 18 - "persistence.py"
Cohesion: 0.22
Nodes (10): RuntimeError, build_persistence_config(), open_checkpoint_saver(), Any, Path, Configuración de persistencia durable para la fábrica., Resuelve la base SQLite y crea solo su directorio padre., Abre un ``SqliteSaver`` para compilar un grafo con checkpoints. (+2 more)

### Community 19 - "git_secure_commit_tool"
Cohesion: 0.09
Nodes (18): _audit_and_measure_progress(), main(), Simulación local del flujo de la fábrica, sin commit ni push reales., _write_initial_files(), ensure_commit_approved(), Any, Políticas de autorización para operaciones Git de la fábrica., Permite continuar solo con una aprobación booleana explícita. La operación Git… (+10 more)

### Community 20 - "Interfaz local"
Cohesion: 0.40
Nodes (4): Arranque, Instalación, Interfaz local, Uso

### Community 33 - "create_initial_state"
Cohesion: 0.21
Nodes (8): add_messages(), create_initial_state(), Any, Contratos de estado compartidos por el flujo Graphify/LangGraph., Valida la forma y los límites del estado completo. Los nodos pueden seguir…, Combina mensajes sin mutar las secuencias de entrada., Crea un estado completo y seguro para iniciar una ejecución., validate_factory_state()

### Community 34 - "FactoryRunRequest"
Cohesion: 0.23
Nodes (8): ArgumentParser, build_parser(), main(), Punto de entrada para ejecutar la fábrica sobre un repositorio local., FactoryRunRequest, CliTests, test_run_request_has_safe_default_iterations(), test_run_request_rejects_invalid_input_before_execution()

### Community 35 - "safe_factory_tools.py"
Cohesion: 0.22
Nodes (9): backup_before_write(), configure_recovery(), get_recovery_directory(), Path, Recuperación no destructiva de archivos modificados por la fábrica., Crea un punto de recuperación único para la ejecución., Guarda una sola copia del archivo antes de su primera modificación., Herramientas de archivos restringidas al workspace de la fábrica. (+1 more)

### Community 36 - "execute_test_command"
Cohesion: 0.25
Nodes (5): execute_test_command(), _is_safe_command(), Ejecuta un comando permitido sin shell y con timeout de 30 segundos., Permite perfiles de verificación, no intérpretes ni operaciones mutantes., ExecuteTestCommandTests

### Community 37 - "build_tasks"
Cohesion: 0.27
Nodes (5): build_tasks(), Any, Conversión pequeña y determinista de requisitos en tareas trazables., Extrae checklists o pasos numerados; si no existen, crea una tarea., TaskPlannerTests

### Community 38 - "AutonomyConfig"
Cohesion: 0.25
Nodes (6): AutonomyMode, AutonomyConfig, _env_bool(), Configuración de autonomía con límites explícitos y seguros., Límites de una ejecución de la fábrica. La instalación solo puede ocurrir…, configure_dependency_installer()

### Community 39 - "dependency_tools.py"
Cohesion: 0.42
Nodes (8): _detect_project_type(), _has_node_dependencies(), install_project_dependencies_tool(), Path, Instalación de dependencias estrictamente limitada al proyecto., Instala dependencias declaradas usando únicamente herramientas locales. No…, _run(), _workspace_path()

### Community 40 - "ui_streamlit.py"
Cohesion: 0.43
Nodes (7): _choose_directory(), _choose_file(), main(), _path_is_readable_file(), Interfaz local para seleccionar un repositorio y ejecutar la fábrica., _select_repository(), _select_requirements_file()

### Community 42 - "ArchitectureBlueprint"
Cohesion: 0.67
Nodes (3): ArchitectureBlueprint, Resultado de arquitectura que acota el trabajo del desarrollador., TypedDict

## Knowledge Gaps
- **50 isolated node(s):** `fabrica-sw`, `Estado`, `Desarrollo`, `Instalación`, `Arranque` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_factory()` connect `runner.py` to `__init__.py`, `FactoryRunRequest`, `safe_factory_tools.py`, `create_initial_state`, `AutonomyConfig`, `ui_streamlit.py`, `git_secure_commit_tool`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `create_initial_state()` connect `create_initial_state` to `__init__.py`, `AuditorTests`, `github_secure_push_tool`, `build_tasks`, `test_workflow_cycle.py`, `test_workflow.py`, `runner.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `FactoryState` connect `__init__.py` to `create_initial_state`, `FactoryStateContractTests`, `architect.py`, `ArchitectureBlueprint`, `persistence.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `FactoryState` (e.g. with `LocalToolNode` and `LocalAutonomousFactory`) actually correct?**
  _`FactoryState` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fabrica-sw`, `Estado`, `Desarrollo` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `validate_safe_path` be split into smaller, more focused modules?**
  _Cohesion score 0.1053763440860215 - nodes in this community are weakly interconnected._
- **Should `__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06018518518518518 - nodes in this community are weakly interconnected._