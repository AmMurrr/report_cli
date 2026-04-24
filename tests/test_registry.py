import pytest

from report_cli.errors import ReportNotFoundError
from report_cli.reports.clickbait import ClickbaitReport
from report_cli.reports.registry import get_report


def test_get_report_returns_clickbait_report() -> None:
    assert isinstance(get_report("clickbait"), ClickbaitReport)


def test_get_report_raises_for_unknown_report() -> None:
    with pytest.raises(ReportNotFoundError, match="Неизвестный отчёт 'unknown'"):
        get_report("unknown")
