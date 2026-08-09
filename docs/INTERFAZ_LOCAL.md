# Interfaz local

La interfaz permite seleccionar una carpeta de repositorio y un archivo de
requerimientos desde una ventana local. Ejecuta el mismo flujo del CLI y
guarda `RUN_REPORT.json` dentro del repositorio seleccionado.

## Instalación

Desde PowerShell, usando el entorno de este proyecto:

```powershell
Set-Location "G:\codex_projects\fabrica_sw"
& ".\.venv\Scripts\pip.exe" install -e ".[runtime,ui]"
```

## Arranque

```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run src\fabrica_sw\ui_streamlit.py
```

Se abrirá el navegador local. La dirección habitual es `http://localhost:8501`.

## Uso

1. Pulsa **Seleccionar carpeta** y elige el repositorio objetivo.
2. Pulsa **Seleccionar archivo** y elige `inst.md`, `requirements.md` o un `.txt`.
3. Revisa la vista previa y pulsa **Iniciar fábrica**.
4. Consulta el estado, el avance, los archivos modificados y el informe.

La interfaz no sube archivos ni ejecuta GitHub por sí sola. La ejecución
continúa respetando `FABRICA_WORKSPACE_DIR`, las herramientas seguras y la
política de aprobación existente.
