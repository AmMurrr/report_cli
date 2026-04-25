from pathlib import Path

import pytest

from report_cli.csv_reader import read_video_metrics
from report_cli.errors import (
    DataFileNotFoundError,
    DataFileReadError,
    InvalidCsvRowError,
)


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


def test_read_video_metrics_raises_for_directory(tmp_path: Path) -> None:
    csv_directory = tmp_path / "metrics.csv"
    csv_directory.mkdir()

    with pytest.raises(DataFileNotFoundError, match="Файл не найден"):
        read_video_metrics([csv_directory])


def test_read_video_metrics_raises_for_read_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    csv_file = tmp_path / "metrics.csv"
    csv_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "First,18.2,35,45200,1240,4.2\n",
        encoding="utf-8",
    )
    original_open = Path.open

    def raise_os_error(self: Path, *args: object, **kwargs: object) -> object:
        if self == csv_file:
            raise OSError("permission denied")

        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", raise_os_error)

    with pytest.raises(DataFileReadError, match="Не удалось прочитать файл"):
        read_video_metrics([csv_file])


def test_read_video_metrics_raises_for_missing_column(tmp_path: Path) -> None:
    csv_file = tmp_path / "missing_column.csv"
    csv_file.write_text(
        "title,retention_rate,views,likes,avg_watch_time\n"
        "First,35,45200,1240,4.2\n",
        encoding="utf-8",
    )

    with pytest.raises(InvalidCsvRowError, match="отсутствует колонка 'ctr'"):
        read_video_metrics([csv_file])


def test_read_video_metrics_raises_for_invalid_number(tmp_path: Path) -> None:
    csv_file = tmp_path / "invalid_number.csv"
    csv_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "First,18.2,35,not-a-number,1240,4.2\n",
        encoding="utf-8",
    )

    with pytest.raises(
        InvalidCsvRowError,
        match="числовое поле содержит некорректное значение",
    ):
        read_video_metrics([csv_file])
