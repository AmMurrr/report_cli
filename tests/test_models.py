from report_cli.models import VideoMetric


def test_video_metric_from_csv_row_converts_numbers() -> None:
    metric = VideoMetric.from_csv_row(
        {
            "title": "Example",
            "ctr": "18.2",
            "retention_rate": "35",
        }
    )

    assert metric == VideoMetric(title="Example", ctr=18.2, retention_rate=35.0)
