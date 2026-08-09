from __future__ import annotations

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fabrica_sw.git_tools import ensure_git_repository
from fabrica_sw.runner import _build_report, _restore_deleted_files
from fabrica_sw.test_profiles import validate_static_web_project
from fabrica_sw.workflow import _detect_changed_files


def test_static_web_project_validation_accepts_html_and_javascript() -> None:
    with TemporaryDirectory() as directory:
        workspace = Path(directory)
        (workspace / "index.html").write_text(
            '<!doctype html><html><body><script src="app.js"></script></body></html>',
            encoding="utf-8",
        )
        (workspace / "app.js").write_text("document.body.append('ok');", encoding="utf-8")

        validation = validate_static_web_project(workspace)
        assert validation is not None
        result, exit_code = validation

        assert exit_code == 0
        assert result.startswith("VALIDATION_STATIC_PASSED")


def test_changed_files_falls_back_to_workspace_listing_without_git() -> None:
    with TemporaryDirectory() as directory:
        workspace = Path(directory)
        (workspace / "index.html").write_text("<html></html>", encoding="utf-8")
        (workspace / ".factory").mkdir()
        (workspace / ".factory" / "internal.txt").write_text("x", encoding="utf-8")

        failed_git = subprocess.CompletedProcess(
            args=["git"], returncode=128, stdout="", stderr="not a repository"
        )
        with patch("fabrica_sw.workflow.WORKSPACE_COMMAND_DIR", workspace), patch(
            "fabrica_sw.workflow.subprocess.run", return_value=failed_git
        ):
            changed_files = _detect_changed_files()

        assert changed_files == ["index.html"]


def test_deleted_files_are_restored_from_snapshot() -> None:
    with TemporaryDirectory() as directory:
        workspace = Path(directory)
        target = workspace / "src" / "app.js"
        target.parent.mkdir()
        target.write_text("original", encoding="utf-8")
        snapshot = {"src/app.js": b"original"}
        target.unlink()

        restored = _restore_deleted_files(workspace, snapshot)

        assert restored == ["src/app.js"]
        assert target.read_text(encoding="utf-8") == "original"


def test_full_mode_can_initialize_a_new_workspace_git_repository() -> None:
    with TemporaryDirectory() as directory:
        workspace = Path(directory)

        result = ensure_git_repository(workspace)

        assert "inicializado" in result
        assert (workspace / ".git").exists()


def test_report_prefers_approved_tasks_from_state() -> None:
    report = _build_report(
        repository=Path("."),
        requirement="crear una página",
        state={"tasks": [{"description": "aprobada", "completed": True}]},
    )

    assert report["tasks"] == [{"description": "aprobada", "completed": True}]
