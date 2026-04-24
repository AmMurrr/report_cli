from report_cli.errors import ReportNotFoundError
from report_cli.reports.base import Report
from report_cli.reports.clickbait import ClickbaitReport

# Регистрация отчётов в формате ['имя отчёта': класс отчёта]
REPORTS: dict[str, Report] = {
    ClickbaitReport.name: ClickbaitReport(),
}


def get_report(report_name: str) -> Report:
    try:
        return REPORTS[report_name]
    except KeyError as error:
        raise ReportNotFoundError(report_name, list(REPORTS)) from error
