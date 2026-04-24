from report_cli.output import format_table


def test_format_table_keeps_headers_for_empty_rows() -> None:
    table = format_table([], ("title", "ctr", "retention_rate"))

    assert "title" in table
    assert "ctr" in table
    assert "retention_rate" in table
