# Persistencia, recuperación y límite de iteraciones

## Política del flujo

La política compartida está en `src/fabrica_sw/workflow_policy.py`.

- `iteration_count < 4` y sin aprobación: la ruta es `developer`.
- `is_approved == true` antes del límite: la ruta es `deploy_and_sync`.
- `iteration_count >= 4`: la ruta es `stop_execution` y el flujo termina en `END`.

El límite se evalúa antes de la aprobación para conservar un cortafuegos
determinista contra ciclos infinitos.

## Guardar y reanudar una ejecución

La fábrica debe compilarse con `SqliteSaver` y usar un `thread_id` estable:

```python
from fabrica_sw.persistence import build_thread_config, open_checkpoint_saver

config = build_thread_config("proyecto_modulo_autenticacion")

with open_checkpoint_saver("factory_state.db") as memory:
    factory = workflow.compile(checkpointer=memory)
    factory.stream(initial_state, config)
```

Después de una interrupción, se vuelve a abrir `factory_state.db` y se usa el
mismo `thread_id`. Así LangGraph identifica el checkpoint de esa ejecución y
puede continuar con el estado persistido. Un `thread_id` nuevo inicia otro
flujo independiente.

La base de datos debe permanecer dentro del espacio de trabajo y no debe
eliminarse durante una recuperación.
