#!/usr/bin/env python3
"""Convert Gnosis Pay CSV export to YNAB CSV format."""

import csv
import re
import sys
from pathlib import Path


REQUIRED_COLUMNS = {"date", "merchant_name", "billing_amount", "status"}
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def normalize_date(value: str) -> str:
    match = DATE_RE.match(value.strip())
    if not match:
        raise ValueError(f"Invalid date value: {value!r}")
    return match.group(1)


def normalize_amount(value: str) -> str:
    amount = value.strip()
    if not amount:
        raise ValueError("Empty billing_amount value")
    return amount.lstrip("+-")


def amount_from_status(status: str, billing_amount: str) -> str | None:
    normalized_status = status.strip()
    absolute_amount = normalize_amount(billing_amount)
    if normalized_status == "Approved":
        return f"-{absolute_amount}"
    if normalized_status == "Reversal":
        return absolute_amount
    if normalized_status == "InsufficientFunds":
        return None
    raise ValueError(f"Unsupported status value: {status!r}")


def convert(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8", newline="") as src:
        reader = csv.DictReader(src)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        with output_path.open("w", encoding="utf-8", newline="") as dst:
            writer = csv.writer(dst, quoting=csv.QUOTE_ALL)
            writer.writerow(["Date", "Payee", "Memo", "Amount"])

            for row in reader:
                amount = amount_from_status(row["status"], row["billing_amount"])
                if amount is None:
                    continue
                writer.writerow(
                    [
                        normalize_date(row["date"]),
                        row["merchant_name"],
                        "",
                        amount,
                    ]
                )


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "Usage: python3 scripts/convert_gnosis_pay_csv_to_ynab.py <input.csv> <output.csv>",
            file=sys.stderr,
        )
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    try:
        convert(input_path, output_path)
    except Exception as exc:  # noqa: BLE001
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
