from pathlib import Path

import pytest

from fabrica_sw.runner import FactoryRunRequest, _build_report


def test_build_report_contains_execution_summary():
    report = _build_report(
        Path("C:/repo"),
        "Crear una función",
        {
            "is_approved": True,
            "validation_available": True,
            "validation_passed": True,
            "validation_exit_code": 0,
            "changed_files": ["src/app.py"],
            "completion_percentage": 100.0,
            "iteration_count": 1,
            "audit_report": "OK",
        },
    )

    assert report["status"] == "PASSED"
    assert report["validation_exit_code"] == 0
    assert report["changed_files"] == ["src/app.py"]
    assert report["tasks"]


def test_run_request_has_safe_default_iterations():
    request = FactoryRunRequest(Path("C:/repo"), "Crear una función")

    assert request.max_iterations == 4


def test_run_request_rejects_invalid_input_before_execution(tmp_path):
    from fabrica_sw.runner import run_factory

    with pytest.raises(ValueError, match="no puede estar vacío"):
        run_factory(FactoryRunRequest(tmp_path, "   "))
