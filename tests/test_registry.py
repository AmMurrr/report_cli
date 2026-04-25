from types import ModuleType, SimpleNamespace

import pytest

from report_cli.errors import DuplicateReportNameError, ReportNotFoundError
from report_cli.reports import registry
from report_cli.reports.base import Report
from report_cli.reports.clickbait import ClickbaitReport
from report_cli.reports.registry import get_report, get_reports


def test_get_report_returns_clickbait_report() -> None:
    assert isinstance(get_report("clickbait"), ClickbaitReport)


def test_get_report_raises_for_unknown_report() -> None:
    with pytest.raises(ReportNotFoundError, match="Неизвестный отчёт 'unknown'"):
        get_report("unknown")


def test_get_reports_raises_for_duplicate_report_name(monkeypatch) -> None:
    first_module = ModuleType("first")
    second_module = ModuleType("second")

    class FirstReport(Report):
        name = "duplicate"
        headers = ("title",)

        def build(self, metrics):
            return []

    class SecondReport(Report):
        name = "duplicate"
        headers = ("title",)

        def build(self, metrics):
            return []

    first_module.FirstReport = FirstReport
    second_module.SecondReport = SecondReport
    modules = {
        "report_cli.reports.first": first_module,
        "report_cli.reports.second": second_module,
    }

    monkeypatch.setattr(
        registry.pkgutil,
        "iter_modules",
        lambda _: [SimpleNamespace(name="first"), SimpleNamespace(name="second")],
    )
    monkeypatch.setattr(registry, "import_module", lambda name: modules[name])

    get_reports.cache_clear()
    try:
        with pytest.raises(
            DuplicateReportNameError,
            match="Найдено несколько отчётов с именем 'duplicate'",
        ):
            get_reports()
    finally:
        get_reports.cache_clear()
