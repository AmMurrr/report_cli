from pathlib import Path

from report_cli.cli import main


def test_cli_outputs_clickbait_report(capsys, tmp_path: Path) -> None:
    first_file = tmp_path / "first.csv"
    second_file = tmp_path / "second.csv"

    first_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "First,25.0,22,254000,8900,2.5\n"
        "Low ctr,9.5,35,31500,890,8.9\n",
        encoding="utf-8",
    )
    second_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "Second,18.2,35,45200,1240,4.2\n"
        "High retention,20.0,40,28900,780,7.8\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--files",
            str(first_file),
            str(second_file),
            "--report",
            "clickbait",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "First" in captured.out
    assert "Second" in captured.out
    assert "Low ctr" not in captured.out
    assert "High retention" not in captured.out
    assert captured.out.index("First") < captured.out.index("Second")


def test_cli_returns_error_for_unknown_report(capsys, tmp_path: Path) -> None:
    csv_file = tmp_path / "metrics.csv"
    csv_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "First,25.0,22,254000,8900,2.5\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--files",
            str(csv_file),
            "--report",
            "unknown",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Неизвестный отчёт 'unknown'" in captured.err


def test_cli_returns_error_for_invalid_csv(capsys, tmp_path: Path) -> None:
    csv_file = tmp_path / "metrics.csv"
    csv_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "First,25.0,22,not-a-number,8900,2.5\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--files",
            str(csv_file),
            "--report",
            "clickbait",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Некорректная строка CSV" in captured.err
    assert "числовое поле содержит некорректное значение" in captured.err
