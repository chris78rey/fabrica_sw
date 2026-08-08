### 4. Conectando Graphify en Modo Autónomo y Bajo Consumo

Para que esta fábrica sea óptima en costo de tokens, no debes usar RAG tradicional releyendo los archivos en cada iteración. En su lugar, usa estas dos funciones de Graphify instaladas en el repositorio local del proyecto:

1. **Git Hook de Sincronización AST (`graphify hook install`)**: Ejecuta este comando una vez en la carpeta de tu código. Esto instalará automáticamente un hook de Git post-commit. Cada vez que el agente Desarrollador compile y guarde con éxito un commit, el hook detectará qué archivos cambiaron y reconstruirá la estructura AST (clases, funciones y llamadas) localmente **sin costo de tokens de IA**. El grafo se mantendrá siempre fresco de forma transparente.
2. **Servidor MCP en segundo plano (`graphify serve`)**: Puedes dejar corriendo en tu servidor el comando: `python -m graphify.serve graphify-out/graph.json --transport stdio`. Esto expone las herramientas nativas de Graphify (`query_graph`, `shortest_path`, `get_node`) como herramientas de LangChain. Tus agentes usarán la API estándar de MCP de LangChain para interrogar al grafo, logrando respuestas precisas y quirúrgicas de la estructura de tu proyecto.

De esta manera, tienes una fábrica de desarrollo **100% autónoma, tolerante a fallas (vía SQLite Checkpoint), segura contra ejecuciones externas (vía MSGPack estricto) y con un consumo óptimo de tokens (vía Graphify MCP y Git Hooks)**, sin depender en absoluto de la infraestructura de Buzz.

---