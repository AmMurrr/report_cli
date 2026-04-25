from pathlib import Path

import pytest

from report_cli.csv_reader import read_video_metrics
from report_cli.errors import DataFileNotFoundError


def test_read_video_metrics_combines_multiple_files(tmp_path: Path) -> None:
    first_file = tmp_path / "first.csv"
    second_file = tmp_path / "second.csv"

    first_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "First,18.2,35,45200,1240,4.2\n"
        "Second,9.5,82,31500,890,8.9\n",
        encoding="utf-8",
    )
    second_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "Third,25.0,22,254000,8900,2.5\n"
        "Fourth,8.5,76,28900,780,7.8\n",
        encoding="utf-8",
    )

    metrics = read_video_metrics([first_file, second_file])

    assert [metric.title for metric in metrics] == [
        "First",
        "Second",
        "Third",
        "Fourth",
    ]
    assert metrics[0].ctr == 18.2
    assert metrics[0].retention_rate == 35
    assert metrics[0].views == 45200
    assert metrics[0].likes == 1240
    assert metrics[0].avg_watch_time == 4.2


def test_read_video_metrics_raises_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(DataFileNotFoundError, match="Файл не найден"):
        read_video_metrics([missing_file])
