import inspect
import pkgutil
from functools import lru_cache
from importlib import import_module

from report_cli import reports
from report_cli.errors import ReportNotFoundError
from report_cli.reports.base import Report

IGNORED_MODULES = {"base", "registry"}


@lru_cache
def get_reports() -> dict[str, Report]:
    discovered_reports: dict[str, Report] = {}

    for module_info in pkgutil.iter_modules(reports.__path__):
        if module_info.name in IGNORED_MODULES:
            continue

        module = import_module(f"{reports.__name__}.{module_info.name}")
        for value in vars(module).values():
            if not _is_report_class(value):
                continue

            report = value()
            discovered_reports[report.name] = report

    return discovered_reports


def get_report(report_name: str) -> Report:
    report_list = get_reports()

    try:
        return report_list[report_name]
    except KeyError as error:
        raise ReportNotFoundError(report_name, list(report_list)) from error


def _is_report_class(value: object) -> bool:
    return (
        inspect.isclass(value)
        and issubclass(value, Report)
        and value is not Report
        and not inspect.isabstract(value)
    )
