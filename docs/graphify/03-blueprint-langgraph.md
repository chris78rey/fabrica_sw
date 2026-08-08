### 3. Blueprint de Implementación en Python (LangGraph)

Este script de Python configura la fábrica con **ejecución duradera (SQLite Checkpointer)** y una directiva de **seguridad estricta para evitar la inyección de código al recuperar estados** (`LANGGRAPH_STRICT_MSGPACK`).

```
import os
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from fabrica_sw.state import FactoryState
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. Activación de Seguridad en la Deserialización de Estado
# Esto evita que código malicioso se ejecute si la base de datos de estados es comprometida
os.environ["LANGGRAPH_STRICT_MSGPACK"] = "true"

# 2. Definición del Estado de la Fábrica
# FactoryState es el contrato canónico compartido por todos los nodos.

# 3. Definición de los Nodos de la Fábrica
def architect_node(state: FactoryState):
    # Aquí el modelo usa herramientas MCP de Graphify para mapear el código
    # Retorna el blueprint arquitectónico
    return {"architecture_blueprint": {"impacted_files": ["src/auth.py"], "dependencies": ["db_pool"]}}

def developer_node(state: FactoryState):
    # Aquí el modelo escribe el código y ejecuta pruebas unitarias locales
    return {
        "source_code_draft": {"src/auth.py": "def login(): pass  # WHY: secure auth entry"},
        "test_results": "OK: 1 test passed",
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def auditor_node(state: FactoryState):
    # Evalúa el código. Si es seguro, aprueba.
    # Si encuentra fallos (ej. vulnerabilidad), rechaza.
    code = state["source_code_draft"]
    # Simulación de auditoría exitosa:
    return {
        "is_approved": True,
        "audit_report": "Código limpio y libre de fallas OWASP."
    }

# Enrutador condicional basado en la decisión del Auditor
def route_audit_decision(state: FactoryState):
    if state["is_approved"]:
        return "commit_code"
    if state["iteration_count"] >= 3:
        return "force_stop" # Evita bucles infinitos de tokens si la IA no logra resolver
    return "developer"

def commit_code_node(state: FactoryState):
    # Aquí puedes escribir físicamente los cambios a disco y hacer el commit de Git
    print("¡Fábrica Autónoma completó el desarrollo de forma óptima y segura!")
    return state

# 4. Construcción y Compilación del Grafo
workflow = StateGraph(FactoryState)

# Agregar nodos
workflow.add_node("architect", architect_node)
workflow.add_node("developer", developer_node)
workflow.add_node("auditor", auditor_node)
workflow.add_node("commit_code", commit_code_node)

# Establecer puntos de entrada y conexiones
workflow.set_entry_point("architect")
workflow.add_edge("architect", "developer")
workflow.add_edge("developer", "auditor")

# Agregar bifurcación condicional basada en la auditoría
workflow.add_conditional_edges(
    "auditor",
    route_audit_decision,
    {
        "developer": "developer",
        "commit_code": "commit_code",
        "force_stop": END
    }
)
workflow.add_edge("commit_code", END)

# 5. Persistencia Duradera con SQLite (Checkpointer)
# Esto permite que si tu máquina se apaga o la API de OpenAI/Anthropic se cae,
# el flujo se reanude exactamente en el examen o archivo donde se quedó
with SqliteSaver.from_conn_string("factory_state.db") as memory:
    factory = workflow.compile(checkpointer=memory)

    # Ejecución de la fábrica con un identificador de hilo único
    config = {"configurable": {"thread_id": "proyecto_modulo_autenticacion"}} #
    initial_input = {
        "user_requirement": "Necesito un sistema de autenticación de dos factores.",
        "iteration_count": 0
    }

    # Arrancar la ejecución duradera
    for event in factory.stream(initial_input, config):
        print(event)
```

---
