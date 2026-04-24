from collections.abc import Iterable, Mapping, Sequence

from tabulate import tabulate


def format_table(
    rows: Iterable[Mapping[str, object]],
    headers: Sequence[str],
) -> str:
    table_rows = [[row.get(header, "") for header in headers] for row in rows]
    return tabulate(table_rows, headers=headers, tablefmt="github")
