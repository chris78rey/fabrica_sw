# Fábrica de Software Segura

Orquestador local para analizar, desarrollar, auditar y preparar la entrega de cambios en un repositorio.

## Estado

El núcleo del workflow y sus herramientas seguras están implementados. La integración operativa con proveedores de modelos y el CLI se incorporarán en la Fase 6.

## Desarrollo

Usa el entorno virtual del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
```

Para instalar las dependencias opcionales del workflow:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[runtime]"
```

