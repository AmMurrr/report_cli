import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from report_cli.app import run
from report_cli.errors import AppError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="report-cli",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        type=Path,
        help="Путь до CSV файлов.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчёта",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        run(files=args.files, report_name=args.report, stdout=sys.stdout)
    except AppError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
