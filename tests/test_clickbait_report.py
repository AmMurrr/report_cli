from report_cli.models import VideoMetric
from report_cli.reports.clickbait import ClickbaitReport


def make_metric(title: str, ctr: float, retention_rate: float) -> VideoMetric:
    return VideoMetric(
        title=title,
        ctr=ctr,
        retention_rate=retention_rate,
        views=100,
        likes=10,
        avg_watch_time=1.5,
    )


def test_clickbait_report_filters_and_sorts_rows() -> None:
    report = ClickbaitReport()
    metrics = [
        make_metric(title="Low ctr", ctr=15.0, retention_rate=20.0),
        make_metric(title="High retention", ctr=20.0, retention_rate=40.0),
        make_metric(title="Second", ctr=18.2, retention_rate=35.0),
        make_metric(title="First", ctr=25.0, retention_rate=22.0),
    ]

    assert report.build(metrics) == [
        {"title": "First", "ctr": 25.0, "retention_rate": 22.0},
        {"title": "Second", "ctr": 18.2, "retention_rate": 35.0},
    ]
