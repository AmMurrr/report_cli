import csv
from collections.abc import Iterable
from pathlib import Path

from report_cli.errors import DataFileNotFoundError, InvalidCsvRowError
from report_cli.models import VideoMetric


def read_video_metrics(files: Iterable[Path]) -> list[VideoMetric]:
    metrics: list[VideoMetric] = []

    for file_path in files:
        if not file_path.exists():
            raise DataFileNotFoundError(file_path)

        with file_path.open(encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    metrics.append(VideoMetric.from_csv_row(row))
                except KeyError as error:
                    column_name = error.args[0]
                    raise InvalidCsvRowError(
                        file_path,
                        reader.line_num,
                        f"отсутствует колонка '{column_name}'",
                    ) from error
                except ValueError as error:
                    raise InvalidCsvRowError(
                        file_path,
                        reader.line_num,
                        "числовое поле содержит некорректное значение",
                    ) from error

    return metrics
