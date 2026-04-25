from abc import ABC, abstractmethod
from report_cli.models import VideoMetric

ReportRow = dict[str, object]


class Report(ABC):
    name: str
    headers: tuple[str, ...]

    @abstractmethod
    def build(self, metrics: list[VideoMetric]) -> list[ReportRow]:
        pass
