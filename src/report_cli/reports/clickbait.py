from report_cli.models import VideoMetric
from report_cli.reports.base import Report, ReportRow


class ClickbaitReport(Report):
    name = "clickbait"
    headers = ("title", "ctr", "retention_rate")

    def build(self, metrics: list[VideoMetric]) -> list[ReportRow]:
        clickbait_metrics = sorted(
            (
                metric
                for metric in metrics
                if metric.ctr > 15 and metric.retention_rate < 40
            ),
            key=lambda metric: metric.ctr,
            reverse=True,
        )

        return [
            {
                "title": metric.title,
                "ctr": metric.ctr,
                "retention_rate": metric.retention_rate,
            }
            for metric in clickbait_metrics
        ]
