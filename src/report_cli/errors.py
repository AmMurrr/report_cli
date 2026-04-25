from pathlib import Path


class AppError(Exception):
    pass


class DataFileNotFoundError(AppError):
    def __init__(self, file_path: Path) -> None:
        super().__init__(f"Файл не найден: {file_path}")


class InvalidCsvRowError(AppError):
    def __init__(self, file_path: Path, line_number: int, reason: str) -> None:
        super().__init__(
            f"Некорректная строка CSV в файле {file_path}, строка {line_number}: "
            f"{reason}"
        )


class DuplicateReportNameError(AppError):
    def __init__(self, report_name: str) -> None:
        super().__init__(f"Найдено несколько отчётов с именем '{report_name}'")


class ReportNotFoundError(AppError):
    def __init__(self, report_name: str, available_reports: list[str]) -> None:
        if available_reports:
            available = ", ".join(sorted(available_reports))
        else:
            available = "none"

        super().__init__(
            f"Неизвестный отчёт '{report_name}'. Доступные отчёты: {available}"
        )
