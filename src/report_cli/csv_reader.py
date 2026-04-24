import csv
from collections.abc import Iterable
from pathlib import Path

from report_cli.errors import DataFileNotFoundError
from report_cli.models import VideoMetric


def read_video_metrics(files: Iterable[Path]) -> list[VideoMetric]:
    metrics: list[VideoMetric] = []

    for file_path in files:
        if not file_path.exists():
            raise DataFileNotFoundError(file_path)

        with file_path.open(encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            metrics.extend(VideoMetric.from_csv_row(row) for row in reader)

    return metrics
