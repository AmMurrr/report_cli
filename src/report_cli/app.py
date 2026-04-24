from pathlib import Path
from typing import TextIO

from report_cli.csv_reader import read_video_metrics
from report_cli.output import format_table
from report_cli.reports.registry import get_report


def run(files: list[Path], report_name: str, stdout: TextIO) -> None:
    report = get_report(report_name)
    metrics = read_video_metrics(files)
    rows = report.build(metrics)

    print(format_table(rows, report.headers), file=stdout)
