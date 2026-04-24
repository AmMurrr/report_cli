from report_cli.models import VideoMetric
from report_cli.reports.clickbait import ClickbaitReport


def test_clickbait_report_filters_and_sorts_rows() -> None:
    report = ClickbaitReport()
    metrics = [
        VideoMetric(title="Low ctr", ctr=15.0, retention_rate=20.0),
        VideoMetric(title="High retention", ctr=20.0, retention_rate=40.0),
        VideoMetric(title="Second", ctr=18.2, retention_rate=35.0),
        VideoMetric(title="First", ctr=25.0, retention_rate=22.0),
    ]

    assert report.build(metrics) == [
        {"title": "First", "ctr": 25.0, "retention_rate": 22.0},
        {"title": "Second", "ctr": 18.2, "retention_rate": 35.0},
    ]
