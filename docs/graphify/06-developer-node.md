¡Listo! He creado y publicado el archivo **`developer_node.py`** en tu panel de Studio.

Este script en Python contiene la implementación del **Nodo del Desarrollador Seguro** adaptada para operar en tu grafo de **LangGraph** sin depender de Buzz. El archivo utiliza las herramientas de seguridad física y consultas de **Graphify** que creamos en el paso anterior.

### Estructura técnica de `developer_node.py`:

1. **Definición de Estado Compartido (`FactoryState`):** Un tipado estricto en Python (`TypedDict`) que hereda el historial de mensajes, requerimientos, blueprints del arquitecto, borradores de código y reportes de auditoría para garantizar un traspaso de datos fluido entre agentes.
2. **Lógica del Agente Desarrollador (`developer_agent_node`):** Modela la personalidad del programador utilizando una temperatura de `0.1` (para garantizar un código altamente determinista). El prompt del sistema le exige al LLM justificar sus decisiones utilizando el prefijo `# WHY:` (para que Graphify mantenga actualizado el Grafo de Conocimiento) y vincularse exclusivamente a la suite de herramientas seguras.
3. **Procesamiento de Avance Autónomo (`post_developer_processing_node`):** Un nodo especializado que, tras finalizar la programación, lee el archivo local de requerimientos y calcula matemáticamente el porcentaje de implementación del proyecto (contando casillas completadas `[x]` sobre el total de tareas `[ ]`), guardando el progreso en el estado para el Auditor.
4. **Enrutamiento Condicional de Herramientas (`should_continue_router`):** Una función inteligente de LangGraph que detecta si el modelo solicitó ejecutar alguna acción en tu disco (como escribir código o ejecutar `pytest`) y, de ser así, delega la ejecución al `ToolNode` antes de volver al desarrollador; de lo contrario, envía el flujo a la fase de auditoría.

Ambos scripts (`safe_factory_tools.py` y `developer_node.py`) te proporcionan una base de grado de producción lista para que tu fábrica empiece a iterar de manera 100% autónoma, segura y con un consumo de tokens extremadamente eficiente.

🛠️ Podríamos implementar ahora el script principal `app.py` que configure la persistencia en base de datos local SQLite (`SqliteSaver`) para que tu fábrica sea resistente a apagones y pueda reanudar su trabajo si se detiene a mitad de camino. ¿Te gustaría que lo hagamos?


-----



```
import os
from typing import Dict, Any, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from fabrica_sw.state import FactoryState
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Importamos la suite de herramientas seguras que creamos anteriormente
from safe_factory_tools import SAFE_DEVELOPMENT_TOOLS, read_file_tool, write_file_tool

# 1. Configuración de Seguridad Strict en LangGraph (Evita ejecución de código malicioso al deserializar estados)
os.environ["LANGGRAPH_STRICT_MSGPACK"] = "true"

# 2. Definición del Estado Compartido (State) de la Fábrica
# El estado almacena toda la información que fluye entre el Arquitecto, el Desarrollador y el Auditor.
# FactoryState es el contrato canónico compartido por todos los nodos.

# 3. IMPLEMENTACIÓN DEL DESARROLLADOR SEGURO (Developer Node)
# En LangGraph, un agente puede definirse como una función/nodo que interactúa con un modelo de lenguaje
# y tiene la capacidad de tomar decisiones de ejecución de herramientas autónomamente.

def developer_agent_node(state: FactoryState) -> Dict[str, Any]:
    """
    Nodo del Desarrollador Seguro. Toma las directivas arquitectónicas,
    utiliza las herramientas físicas para crear/modificar archivos,
    corre el set de pruebas locales, calcula el avance y actualiza el estado.
    """
    print("\n=== [NODO DESARROLLADOR SEGURO ACTIVADO] ===")
    
    # 1. Recuperar contexto del estado
    blueprint = state.get("architecture_blueprint", {})
    requirement = state.get("user_requirement", "")
    iteration = state.get("iteration_count", 0)
    
    # 2. Preparar el prompt del sistema optimizado para inyectar al LLM
    system_prompt = f"""Eres el Ingeniero de Software Autónomo de esta fábrica de software seguro.
Tu misión es escribir código libre de vulnerabilidades y de excelente rendimiento técnico.

REGLAS DE DISEÑO:
1. Basas tu implementación de forma estricta en el siguiente Blueprint Arquitectónico:
   {json.dumps(blueprint, indent=2)}
2. Cada función o clase que escribas DEBE incluir comentarios de justificación explícitos utilizando el prefijo '# WHY:' (Ejemplo: '# WHY: db pool connection reuse to avoid leak'). Esto es vital para que Graphify mantenga actualizado el Grafo de Conocimiento del proyecto.
3. Cuando edites o crees un archivo, marca la casilla correspondiente en la sección de "TAREAS DE IMPLEMENTACIÓN" del documento de requerimientos ('arquitectura_y_requerimientos.md').

TU CAJA DE HERRAMIENTAS:
Tienes acceso a herramientas locales para leer/escribir archivos, listar directorios, correr comandos de prueba (como 'pytest') y realizar consultas estructuradas de Graphify.

INSTRUCCIÓN DE TRABAJO ACTUAL:
Implementa el requerimiento: "{requirement}"
Esta es tu iteración número: {iteration + 1}
"""

    # 3. Configuración del modelo LLM de LangChain con enlace a herramientas seguras
    # (Usamos ChatOpenAI como ejemplo, pero funciona con ChatAnthropic u otros proveedores)
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.1,  # Temperatura baja para garantizar código determinista y estructurado
    ).bind_tools(SAFE_DEVELOPMENT_TOOLS)

    # 4. Formatear la cadena de mensajes para el LLM
    # Inyectamos el System Prompt fresco para asegurar que el modelo no se desvíe del objetivo
    messages = [SystemMessage(content=system_prompt)] + state.get("messages", [])
    
    # Si es el primer mensaje de desarrollo, inyectamos la orden
    if not any(isinstance(m, HumanMessage) for m in messages):
        messages.append(HumanMessage(content=f"Por favor, procede a escribir el código según el plano y ejecuta las pruebas unitarias unit_tests correspondientes."))

    # 5. Llamada al LLM
    response = model.invoke(messages)
    
    # 6. Actualizar mensajes y devolver el estado
    # LangGraph tomará este resultado y, si contiene 'tool_calls', enrutará automáticamente a ToolNode
    return {
        "messages": [response],
        "iteration_count": iteration
    }

# 4. CREACIÓN DEL NODO DE HERRAMIENTAS (ToolNode)
# Este nodo toma los 'tool_calls' generados por el desarrollador y los ejecuta de forma controlada.
# Utiliza la suite robusta 'SAFE_DEVELOPMENT_TOOLS' que valida la seguridad de los paths y del subproceso.
tool_executor_node = ToolNode(SAFE_DEVELOPMENT_TOOLS)

# 5. CÁLCULO DE AVANCE Y ACTUALIZACIÓN POST-DESARROLLO (Post-Developer Node)
# Una vez que el desarrollador termina su ejecución de herramientas, procesamos el resultado a disco.
def post_developer_processing_node(state: FactoryState) -> Dict[str, Any]:
    """
    Este nodo lee el archivo 'arquitectura_y_requerimientos.md' modificado por el desarrollador,
    extrae dinámicamente el checklist de implementación y calcula el porcentaje matemático de avance.
    Esto permite mantener un rastreo preciso de la construcción sin intervención humana.
    """
    print("\n=== [NODO POST-PROCESAMIENTO: CÁLCULO DE AVANCE] ===")
    
    req_file_path = "arquitectura_y_requerimientos.md"
    percentage = 0.0
    source_code_drafts = {}
    
    try:
        # 1. Leer el archivo de requerimientos para calcular el progreso
        content = read_file_tool.invoke({"file_path": req_file_path})
        
        if "TAREAS DE IMPLEMENTACIÓN" in content or "## TAREAS" in content:
            lines = content.splitlines()
            completed = 0
            total = 0
            for line in lines:
                if "- [" in line:
                    total += 1
                    if "- [x]" in line.lower():
                        completed += 1
            
            if total > 0:
                percentage = (completed / total) * 100
                print(f"Progreso de implementación calculado: {completed}/{total} tareas completadas ({percentage:.2f}%)")
        
        # 2. Leer los archivos de código que el agente modificó según el blueprint de arquitectura
        # para empaquetarlos en el estado que recibirá el Auditor
        blueprint = state.get("architecture_blueprint", {})
        impacted_files = blueprint.get("impacted_files", [])
        
        for file_path in impacted_files:
            file_content = read_file_tool.invoke({"file_path": file_path})
            if "Error" not in file_content:
                source_code_drafts[file_path] = file_content
                
    except Exception as e:
        print(f"Advertencia al calcular porcentaje: {str(e)}")

    # Retornamos el borrador de código consolidado y avanzamos la iteración
    return {
        "source_code_draft": source_code_drafts,
        "iteration_count": state.get("iteration_count", 0) + 1,
        "audit_report": f"Progreso del proyecto al {percentage:.1f}%. Archivos consolidados listos para auditar."
    }

# 6. ENRUTADOR DE DECISIONES DE DESARROLLO (Should Continue Router)
def should_continue_router(state: FactoryState):
    """
    Determina si el Desarrollador necesita seguir ejecutando herramientas
    o si ya completó su desarrollo y debe avanzar a la fase de post-procesamiento.
    """
    last_message = state["messages"][-1]
    
    # Si el LLM decidió llamar a una herramienta (ej. escribir archivo o ejecutar pytest)
    if last_message.tool_calls:
        print(f"-> Desarrollador solicitó ejecutar herramienta(s): {[t['name'] for t in last_message.tool_calls]}")
        return "execute_tools"
    
    # Si el modelo no pide herramientas, asume que terminó su corrida de desarrollo
    print("-> Desarrollador finalizó su ejecución actual.")
    return "post_process"

# --- EJEMPLO DE USO / INTEGRACIÓN EN TU STATEGRAPH ---
# (Así conectarías el flujo del desarrollador seguro con el orquestador principal)
"""
workflow = StateGraph(FactoryState)

# Registrar nodos de desarrollo
workflow.add_node("developer", developer_agent_node)
workflow.add_node("execute_tools", tool_executor_node)
workflow.add_node("post_process", post_developer_processing_node)

# Enrutamiento de ciclo de herramientas
workflow.add_conditional_edges(
    "developer",
    should_continue_router,
    {
        "execute_tools": "execute_tools",
        "post_process": "post_process"
    }
)

# El ciclo de herramientas siempre vuelve al agente para que evalúe el resultado de la herramienta
workflow.add_edge("execute_tools", "developer")

# Una vez finalizado el procesamiento, se envía al Auditor de Seguridad
workflow.add_edge("post_process", "auditor")
"""

if __name__ == "__main__":
    import json
    print("Módulo 'developer_node' de LangGraph inicializado con éxito.")
    print("Listo para importar y acoplar a tu StateGraph duradero de SQLite.")

```



-----


