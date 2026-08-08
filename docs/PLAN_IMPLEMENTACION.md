# Plan de implementación de la fábrica segura

Checklist vivo para avanzar por incrementos pequeños y verificables. El orden está basado en las relaciones consultadas en `graphify-out/graph.json`.

## Cómo marcar el avance

- `[ ]` Pendiente.
- `[x]` Completada y verificada.
- Mantener una tarea sin marcar hasta que exista evidencia: código, prueba o comando ejecutado.

## 0. Base del proyecto

- [x] T0.1 Crear el entorno virtual del proyecto en `.venv`.
- [x] T0.2 Instalar y fijar Graphify en el entorno del proyecto.
- [x] T0.3 Generar `graphify-out/graph.json`, `GRAPH_REPORT.md` y `graph.html`.
- [x] T0.4 Dividir la documentación en piezas lógicas dentro de `docs/graphify/`.
- [x] T0.5 Asignar nombres a las seis comunidades del grafo y documentar la arquitectura inferida.

## 1. Arquitectura y estado persistente

- [x] T1.1 Consolidar un único contrato de `FactoryState` para blueprint, desarrollo y aplicación final.
  - Evidencia: `src/fabrica_sw/state.py` define `FactoryState` y `ArchitectureBlueprint`; `docs/graphify/03-blueprint-langgraph.md`, `docs/graphify/06-developer-node.md` y `docs/graphify/07-safe-factory-app.md` importan el contrato compartido; `tests/test_state.py` valida sus campos.
- [x] T1.2 Definir y validar los campos `architecture_blueprint`, `impacted_files`, `source_code_draft`, `test_results`, `is_approved`, `iteration_count`, `completion_percentage` y `messages`.
  - Evidencia: `create_initial_state()` establece valores iniciales seguros y `validate_factory_state()` valida presencia, tipos y límites; cobertura en `tests/test_state.py`.
- [x] T1.3 Confirmar la decisión de persistencia: `SqliteSaver`, `factory_state.db` y `thread_id`.
  - Evidencia: `src/fabrica_sw/persistence.py` centraliza `FACTORY_STATE_DB`, valida `thread_id`, prepara la ruta y abre `SqliteSaver`; `tests/test_state.py` verifica la configuración y la creación segura del directorio.
- [x] T1.4 Documentar recuperación después de interrupciones y límite máximo de iteraciones.
  - Evidencia: `src/fabrica_sw/workflow_policy.py` fija `MAX_ITERATIONS = 4` y las rutas; `docs/graphify/10-persistencia-recuperacion.md` documenta `SqliteSaver`, `factory_state.db` y la reanudación con el mismo `thread_id`; `tests/test_state.py` cubre rutas normales, aprobación, límite y entradas inválidas.

## 2. Herramientas de ejecución segura

- [x] T2.1 Implementar o verificar `validate_safe_path` contra `WORKSPACE_DIR`.
  - Evidencia: `src/fabrica_sw/safe_paths.py` resuelve rutas, aplica la frontera de `WORKSPACE_DIR` y sigue enlaces simbólicos; `tests/test_safe_paths.py` cubre rutas internas, escape `..`, rutas absolutas externas, enlaces y rutas vacías.
- [x] T2.2 Verificar `read_file_tool`, `write_file_tool` y `list_directory_tool`.
  - Evidencia: `src/fabrica_sw/safe_factory_tools.py` implementa lectura y escritura UTF-8, listado ordenado y mensajes de error; `tests/test_safe_factory_tools.py` cubre contenido UTF-8, rutas inexistentes, directorios, creación de padres, listado y rechazo de rutas externas.
- [x] T2.3 Verificar `execute_test_command` con directorio controlado y tiempo máximo.
  - Evidencia: `src/fabrica_sw/safe_factory_tools.py` usa lista de comandos permitidos, `subprocess.run` sin shell, `WORKSPACE_COMMAND_DIR` y timeout de 30 segundos; `tests/test_execute_test_command.py` cubre ejecución, argumentos inválidos, bloqueo y timeout.
- [x] T2.4 Verificar `graphify_query_tool` y `graphify_shortest_path_tool` usando el Graphify local.
  - Evidencia: `src/fabrica_sw/safe_factory_tools.py` usa el ejecutable Graphify del `.venv`, `graphify-out/graph.json`, `subprocess.run` sin shell y timeout de 15 segundos; `tests/test_graphify_tools.py` cubre grafo ausente, validación, errores y argumentos; la CLI real ejecutó `query` y `path` correctamente.
- [x] T2.5 Registrar todas las herramientas en `SAFE_DEVELOPMENT_TOOLS`.
  - Evidencia: `src/fabrica_sw/safe_factory_tools.py` exporta las seis herramientas en orden estable; `tests/test_tool_registry.py` verifica registro completo, unicidad y que todos sean invocables.

## 3. Flujo LangGraph seguro

- [x] T3.1 Implementar `architect_node` para consultar Graphify antes de modificar archivos.
  - Evidencia: `src/fabrica_sw/architect.py` consulta `graphify_query_tool` antes de invocar el modelo, genera `architecture_blueprint` y no ejecuta escritura ni Git; `tests/test_architect.py` verifica orden de consulta, modo sin LangChain y validación del requerimiento.
- [x] T3.2 Implementar `developer_node` y su despacho mediante `ToolNode`.
  - Evidencia: `src/fabrica_sw/developer.py` y `tests/test_developer.py`.
  - Verificación: `python -m unittest discover -s tests -v` (42 pruebas OK).
- [x] T3.3 Implementar `should_continue_router` y el retorno de herramientas al nodo correcto.
  - Evidencia: `src/fabrica_sw/developer.py` y `tests/test_developer.py`.
  - Verificación: router probado para llamadas de herramientas y finalización.
- [x] T3.4 Implementar `auditor_node` para inspeccionar archivos, pruebas y decisiones arquitectónicas.
  - Evidencia: `src/fabrica_sw/auditor.py`, `tests/test_auditor.py` y exportación desde `src/fabrica_sw/__init__.py`.
  - Verificación: auditoría conservadora sin modelo, extracción segura de JSON, cálculo de checklist y uso de herramientas registradas.
- [x] T3.5 Implementar `evaluate_workflow_router` para aprobación, corrección, despliegue o finalización.
  - Evidencia: `src/fabrica_sw/workflow_policy.py`, exportación desde `src/fabrica_sw/__init__.py` y pruebas de rutas en `tests/test_state.py`.
  - Verificación: aprobación dirige a despliegue, rechazo dirige a desarrollador y el límite dirige a detención; se conserva alias compatible.
- [x] T3.6 Probar el ciclo Desarrollador → Auditor → corrección con límite de iteraciones.
  - Evidencia: `tests/test_workflow_cycle.py` ejecuta el ciclo con modelos simulados, verifica corrección seguida de despliegue y confirma la detención en `MAX_ITERATIONS`.
  - Verificación: `python -m unittest discover -s tests -v` y compilación de `src` y `tests` sin errores.

## 4. Sincronización Git y Graphify

- [x] T4.1 Permitir commit únicamente cuando `is_approved` sea verdadero.
  - Evidencia: `src/fabrica_sw/git_policy.py` expone `ensure_commit_approved`, una compuerta reutilizable que exige aprobación booleana explícita antes de cualquier commit; `tests/test_git_policy.py` cubre aprobación, rechazo y tipos inválidos.
  - Verificación: `python -m unittest discover -s tests -v` y compilación de `src` y `tests` sin errores.
- [x] T4.2 Implementar `git_secure_commit_tool` con selección explícita de cambios.
  - Evidencia: `src/fabrica_sw/git_tools.py` exige aprobación, valida las rutas dentro del workspace y ejecuta `git add -- <archivos>` seguido de `git commit -m`, sin `shell` ni selección global (`.`); `tests/test_git_tools.py` cubre aprobación, rutas externas, fallo de `git add` y selección explícita.
  - Verificación: `python -m unittest discover -s tests -v` (61 pruebas OK) y compilación de `src` y `tests` sin errores.
- [x] T4.3 Implementar `github_secure_push_tool` dependiendo de un commit seguro.
  - Evidencia: `src/fabrica_sw/github_safe_pusher.py` exige aprobación, `GITHUB_TOKEN`, una referencia de rama segura y un `HEAD` local verificable antes de ejecutar `git push`; el token no se incluye en comandos y se enmascara en resultados.
  - Verificación: `python -m unittest discover -s tests -v` y compilación de `src` y `tests` sin errores.
- [x] T4.4 Activar o verificar el Git Hook que reconstruye el grafo después del commit aprobado.
  - Evidencia: `.githooks/post-commit` reconstruye el grafo con el `graphify.exe` del `.venv` usando `update --code-only --no-cluster`; `scripts/install-git-hooks.ps1` configura `core.hooksPath` sin tocar hooks globales y `tests/test_graphify_hook.py` verifica ambos contratos.
  - Verificación: `python -m unittest discover -s tests -v` y compilación de `src` y `tests` sin errores. Este workspace aún no contiene `.git`, por lo que la activación queda preparada para el repositorio Git real.

## 5. Validación y entrega

- [x] T5.1 Ejecutar la simulación de `simulate_factory_run.py` en un repositorio temporal.
  - Evidencia: `simulate_factory_run.py` crea `sandbox_test_repo`, genera `auth_security.py`, valida su sintaxis, calcula 66.7% de avance y mantiene commit/push en modo simulado sin credenciales ni red.
  - Verificación: ejecución con `.venv\\Scripts\\python.exe simulate_factory_run.py` finalizada con código 0; el sandbox temporal fue eliminado al terminar.
- [x] T5.2 Verificar `hash_password_secure` y `validate_password_complexity` con pruebas positivas y negativas.
  - Evidencia: `src/fabrica_sw/auth_security.py` centraliza el hashing PBKDF2 con sal aleatoria y la validación de complejidad; `tests/test_auth_security.py` cubre casos válidos e inválidos.
  - Verificación: 5 pruebas de seguridad incluidas en una suite total de 73; `compileall` finalizado sin errores.
- [x] T5.3 Confirmar que el repositorio temporal se limpia al terminar la simulación.
  - Evidencia: `tests/test_simulation.py` ejecuta la simulación sobre un sandbox aislado y confirma que desaparece al finalizar.
  - Verificación: la prueba de limpieza y la simulación manual finalizan con código 0.
- [x] T5.4 Ejecutar una prueba de extremo a extremo desde arquitectura hasta sincronización.
  - Evidencia: `tests/test_end_to_end_workflow.py` recorre Arquitecto → Desarrollador → Auditor → política de despliegue → commit y push simulados.
  - Verificación: 75 pruebas OK y compilación sin errores; el flujo aprueba el estado auditado y ejecuta las dos etapas de Git mediante despachos controlados.
- [x] T5.5 Actualizar Graphify con `--update` y revisar que no existan endpoints huérfanos ni relaciones duplicadas.
  - Evidencia: `graphify update . --no-cluster` reconstruyó `graphify-out/graph.json` con 313 nodos y 647 relaciones.
  - Verificación: diagnóstico Graphify sin duplicados exactos; los 21 pares con relaciones distintas son variantes intencionales de importación/reexportación, y los 99 endpoints ausentes apuntan únicamente a módulos externos o de la biblioteca estándar.

## T6. Orquestación ejecutable derivada de Graphify

- [x] T6.1 Conectar Arquitecto, Desarrollo, herramientas, Auditoría y política de entrega en `build_autonomous_factory`.
  - Evidencia: `src/fabrica_sw/workflow.py` implementa el grafo LangGraph y `LocalAutonomousFactory` como fallback cuando LangGraph no está instalado.
  - Seguridad: la etapa `deploy_and_sync_node` solo marca la entrega como preparada; commit, push y Graphify siguen siendo invocaciones explícitas.

## Criterio de avance

Una tarea se marca con `[x]` cuando su resultado está comprobado. Para cada tarea conviene anotar debajo el comando, prueba o archivo que sirve como evidencia.

## Evidencia usada para ordenar las tareas

- `LangGraph architecture` se relaciona con Graphify, LangChain y el checkpointer SQLite/Postgres en `docs/graphify/01-contexto-arquitectura.md`.
- `auditor_node` enruta hacia `commit_code_node` en `docs/graphify/03-blueprint-langgraph.md`.
- `github_secure_push_tool` llama a `git_secure_commit_tool` en `docs/graphify/08-github-safe-pusher.md`.
- Los Git Hooks se relacionan con la reconstrucción del grafo en `docs/graphify/04-integracion-graphify.md`.

## T6.2 Verificación del constructor de orquestación

- [x] T6.2 Ejecutar el flujo completo mediante el fallback local cuando LangGraph no está instalado.
  - Evidencia: `tests/test_workflow.py` valida Arquitecto → Desarrollador → Auditor → entrega preparada.
  - Verificación: suite completa con 78 pruebas OK y `compileall` sin errores.

## T7. Confiabilidad del ciclo de herramientas

- [x] T7.1 Conservar el historial de mensajes del Desarrollador después de ejecutar herramientas.
  - Evidencia: `src/fabrica_sw/developer.py` incorpora los mensajes previos y solo agrega el requerimiento al iniciar la fase; los resultados de herramientas llegan al siguiente `model.invoke`.
  - Verificación: `tests/test_developer.py::test_developer_preserves_previous_messages_after_tool_execution`.
- [x] T7.2 Limitar ciclos repetitivos de herramientas.
  - Evidencia: `FactoryState.tool_round_count` y `_execute_tools_with_limit` detienen el flujo tras 8 rondas y dejan un mensaje explícito para Auditoría.
  - Verificación: `tests/test_workflow.py::test_tool_round_limit_stops_repeated_calls`; suite completa con 78 pruebas OK.

## T8. Herramientas del Auditor

- [x] T8.1 Separar el ejecutor de herramientas del Auditor del ejecutor del Desarrollador.
  - Evidencia: `src/fabrica_sw/auditor.py` define `AUDITOR_TOOLS` únicamente con lectura, pruebas y consultas Graphify; `src/fabrica_sw/workflow.py` crea un ejecutor independiente.
- [x] T8.2 Implementar el ciclo `auditor -> herramientas -> auditor` en fallback local y LangGraph.
  - Evidencia: `auditor_should_continue_router` y el nodo `audit_execute_tools` ejecutan llamadas antes de aplicar `evaluate_workflow_router`.
- [x] T8.3 Conservar historial y limitar rondas de herramientas.
  - Evidencia: `auditor_node` reutiliza mensajes previos y `_execute_tools_with_limit` aplica el límite común de 8 rondas.
- [x] T8.4 Probar lectura y enrutamiento del Auditor.
  - Evidencia: `tests/test_workflow.py` simula `read_file_tool`, `tests/test_auditor.py` verifica el router y la suite completa tiene 80 pruebas OK.

## T9. Permisos por rol y blueprint estructurado

- [x] T9.1 Separar las herramientas del Arquitecto en lectura y consultas Graphify.
  - Evidencia: `src/fabrica_sw/architect.py` define `ARCHITECT_TOOLS` sin escritura, ejecución de comandos ni Git.
- [x] T9.2 Exigir una respuesta arquitectónica estructurada y conservar fallback de texto.
  - Evidencia: `architect_node` normaliza `summary`, `impacted_files`, `dependencies` y `rules` en `architecture_blueprint`.
- [x] T9.3 Probar la allowlist y el parseo del blueprint.
  - Evidencia: `tests/test_architect.py`; suite completa con 81 pruebas OK y compilación sin errores.

## T11. Endurecimiento de ejecucion y sincronizacion Git

- [x] T11.1 Autenticar el push mediante `GIT_ASKPASS` efimero sin incluir el token en argumentos ni archivos persistentes.
  - Evidencia: `src/fabrica_sw/github_safe_pusher.py` crea un helper temporal, usa `GIT_TERMINAL_PROMPT=0` y elimina el helper al finalizar.
  - Verificacion: `tests/test_github_safe_pusher.py` comprueba el entorno del proceso y la ausencia del token en el comando.
- [x] T11.2 Restringir `execute_test_command` a perfiles de inspeccion y pruebas.
  - Evidencia: `src/fabrica_sw/safe_factory_tools.py` bloquea `python -c`, instaladores y operaciones Git mutantes; conserva unittest, pytest y herramientas de analisis.
  - Verificacion: `tests/test_execute_test_command.py` cubre ejecucion permitida, rechazo de codigo arbitrario y timeout.
- [x] T11.3 Verificar la suite y dejar Graphify actualizado.
  - Evidencia: 83 pruebas OK y `compileall` sin errores; Graphify se actualiza despues de este cambio.

## Siguiente fase

Implementar Fase 4: consolidar archivos modificados y resultados de pruebas antes de la Auditoría.

## Próxima tarea sugerida

Implementar T7.3: separar herramientas por rol y habilitar el ciclo `auditor → herramientas → auditor`.
## T10. Consolidación de evidencia del Desarrollador

- [x] T10.1 Consolidar `source_code_draft` a partir de `architecture_blueprint.impacted_files`.
  - Evidencia: `src/fabrica_sw/workflow.py::consolidate_developer_evidence` lee únicamente los archivos impactados y deduplica sus rutas.
- [x] T10.2 Ejecutar y conservar `test_results` antes de la Auditoría.
  - Evidencia: el flujo local y LangGraph ejecutan la consolidación entre Desarrollo y Auditoría.
- [x] T10.3 Probar la consolidación y evitar recursión en la suite.
  - Evidencia: `tests/test_workflow.py`; suite completa con 82 pruebas OK y `compileall` sin errores.

## T12. Empaquetado y configuración operativa

- [x] T12.1 Declarar el proyecto como paquete instalable mediante `pyproject.toml`.
  - Evidencia: `pyproject.toml` declara metadatos, Python mínimo 3.11, descubrimiento de paquetes en `src/` y extras de runtime/desarrollo.
- [x] T12.2 Documentar variables de entorno sin incluir credenciales.
  - Evidencia: `.env.example` contiene únicamente nombres y valores vacíos; `.gitignore` protege `.env` y conserva `.env.example`.
- [x] T12.3 Implementar la fábrica de modelos para OpenAI y OpenRouter.
  - Evidencia: `src/fabrica_sw/model_factory.py` valida proveedor, credencial, temperatura y tokens; construye `ChatOpenAI` de forma perezosa para OpenAI y OpenRouter. `tests/test_model_factory.py` cubre configuración, errores y construcción sin red; suite completa con 89 pruebas OK.
- [x] T12.4 Crear el ejecutable CLI para repositorio y requerimiento.
  - Evidencia: `src/fabrica_sw/cli.py` expone `fabrica-sw`, valida el repositorio, fija el workspace antes de importar herramientas, ejecuta el flujo y devuelve un resumen JSON sin hacer commit ni push.
- [ ] T12.5 Sustituir referencias históricas de verificación y actualizar Graphify tras cerrar la fase.

## Siguiente fase

Implementar la integración operativa multiproveedor y multiproyecto.
