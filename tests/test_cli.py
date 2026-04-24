from report_cli.cli import main


def test_cli_outputs_clickbait_report(capsys) -> None:
    exit_code = main(
        [
            "--files",
            "tests/data/stats1.csv",
            "tests/data/stats2.csv",
            "--report",
            "clickbait",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Секрет который скрывают тимлиды" in captured.out
    assert "Я бросил IT и стал фермером" in captured.out
    assert "Почему сеньоры не носят галстуки" not in captured.out
    assert "Рефакторинг выходного дня" not in captured.out
    assert captured.out.index("Секрет который скрывают тимлиды") < captured.out.index(
        "Я бросил IT и стал фермером"
    )


def test_cli_returns_error_for_unknown_report(capsys) -> None:
    exit_code = main(
        [
            "--files",
            "tests/data/stats1.csv",
            "--report",
            "unknown",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Неизвестный отчёт 'unknown'" in captured.err
