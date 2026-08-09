"""Interfaz local para seleccionar un repositorio y ejecutar la fábrica."""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from .runner import FactoryRunRequest, run_factory
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from fabrica_sw.runner import FactoryRunRequest, run_factory


def _choose_directory() -> str:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return filedialog.askdirectory(title="Selecciona el repositorio") or ""
    finally:
        root.destroy()


def _choose_file() -> str:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return filedialog.askopenfilename(
            title="Selecciona el archivo de requerimientos",
            filetypes=[("Markdown y texto", "*.md *.txt *.rst"), ("Todos los archivos", "*.*")],
        ) or ""
    finally:
        root.destroy()


def _path_is_readable_file(value: str) -> bool:
    path = Path(value).expanduser()
    return path.is_file() and os.access(path, os.R_OK)


def _select_repository() -> None:
    import streamlit as st
    selected = _choose_directory()
    if selected:
        st.session_state["repository"] = selected


def _select_requirements_file() -> None:
    import streamlit as st
    selected = _choose_file()
    if selected:
        st.session_state["requirements_file"] = selected


def main() -> None:
    try:
        import streamlit as st
    except ImportError as exc:
        raise SystemExit(
            "Falta Streamlit. Instala la interfaz con: python -m pip install -e \".[runtime,ui]\""
        ) from exc

    st.set_page_config(page_title="Fábrica SW", page_icon="🏭", layout="wide")
    st.title("Fábrica de Software")
    st.caption("Selecciona un repositorio y un archivo de requerimientos para iniciar una ejecución segura.")

    st.session_state.setdefault("repository", "")
    st.session_state.setdefault("requirements_file", "")
    with st.sidebar:
        st.header("Entrada")
        st.button("Seleccionar carpeta", on_click=_select_repository, use_container_width=True)
        repository = st.text_input("Repositorio", key="repository", placeholder=r"G:\codex_projects\mi_proyecto")
        st.button("Seleccionar archivo", on_click=_select_requirements_file, use_container_width=True)
        requirements_file = st.text_input("Archivo de requerimientos", key="requirements_file", placeholder=r"G:\codex_projects\mi_proyecto\inst.md")
        max_iterations = st.number_input("Máximo de iteraciones", min_value=1, max_value=20, value=4)

    repository_path = Path(repository).expanduser() if repository else None
    requirements_path = Path(requirements_file).expanduser() if requirements_file else None
    if repository_path and not repository_path.is_dir():
        st.error(f"El repositorio no existe o no es una carpeta: {repository_path}")
    if requirements_path and not _path_is_readable_file(requirements_file):
        st.error(f"No se puede leer el archivo de requerimientos: {requirements_path}")
    if requirements_path and _path_is_readable_file(requirements_file):
        try:
            preview = requirements_path.read_text(encoding="utf-8")
            with st.expander("Vista previa del requerimiento", expanded=True):
                st.code(preview[:6000], language="markdown")
        except UnicodeError as exc:
            st.error(f"El archivo debe estar en UTF-8: {exc}")

    can_run = bool(repository_path and repository_path.is_dir() and requirements_path and _path_is_readable_file(requirements_file))
    if st.button("Iniciar fábrica", type="primary", disabled=not can_run, use_container_width=True):
        status_box = st.status("Preparando ejecución...", expanded=True)
        progress_bar = st.progress(0, text="Avance de la fábrica: 0%")
        current_action = st.empty()
        event_log = st.empty()
        events: list[str] = []

        def show_factory_event(event: dict) -> None:
            progress = max(0, min(100, int(event.get("progress", 0))))
            message = event.get("message", "Procesando...")
            stage = event.get("stage", "running")
            task = event.get("task") or event.get("task_id")
            iteration = event.get("iteration")
            suffix = f" · Tarea: {task}" if task else ""
            suffix += f" · Iteración: {iteration}" if iteration is not None else ""
            progress_bar.progress(progress, text=f"Avance de la fábrica: {progress}%")
            current_action.info(f"{message}{suffix}")
            marker = "✗" if event.get("blocked") else "✓"
            events.append(f"{marker} [{stage}] {message}")
            event_log.code("\n".join(events[-20:]))
            status_box.update(label=message, state="running", expanded=True)

        try:
            requirement = requirements_path.read_text(encoding="utf-8")
            result = run_factory(
                FactoryRunRequest(
                    repository=repository_path,
                    requirement=requirement,
                    max_iterations=int(max_iterations),
                ),
                on_event=show_factory_event,
            )
            st.session_state["last_report"] = result.report
            if result.report["status"] == "PASSED":
                status_box.update(label="Ejecución terminada correctamente", state="complete", expanded=False)
                progress_bar.progress(100, text="Ejecución completada")
            else:
                status_box.update(label=f"Ejecución bloqueada: {result.report['status']}", state="error", expanded=True)
                st.warning(result.report.get("audit_report") or "La auditoría no aprobó la ejecución.")
        except (OSError, ValueError, UnicodeError) as exc:
            status_box.update(label="La ejecución terminó con un error", state="error", expanded=True)
            st.error(f"La ejecución no pudo iniciarse o terminó con error: {exc}")
        except Exception as exc:
            status_box.update(label="La ejecución terminó con un error", state="error", expanded=True)
            st.exception(exc)

    report = st.session_state.get("last_report")
    if report:
        st.subheader("Resultado")
        columns = st.columns(3)
        columns[0].metric("Estado", report["status"])
        columns[1].metric("Avance", f"{report['completion_percentage']:.1f}%")
        columns[2].metric("Iteraciones", report["iteration_count"])
        st.json(report)
        graph_html = Path(report["repository"]) / "graphify-out" / "graph.html"
        if graph_html.is_file() and st.button("Abrir grafo Graphify"):
            os.startfile(str(graph_html))
            st.info(f"Grafo abierto: {graph_html}")


if __name__ == "__main__":
    main()
