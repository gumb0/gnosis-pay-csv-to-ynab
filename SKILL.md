---
name: gnosis-pay-csv-to-ynab
description: Convert Gnosis Pay CSV exports into YNAB-compatible CSV files. Use when working with transaction files that include columns like `date`, `merchant_name`, and `billing_amount`, and you need YNAB columns `Date,Payee,Memo,Amount` with date normalized to `YYYY-MM-DD` and amount inverted to negative.
---

# Gnosis Pay CSV To YNAB

Run the converter script to transform Gnosis Pay exports into YNAB import format.

## Convert CSV

1. Run:

```bash
python3 scripts/convert_gnosis_pay_csv_to_ynab.py <input.csv> <output.csv>
```

2. Import the generated CSV into YNAB.

## Field Mapping

- `Date`: take from source `date` column; strip to `YYYY-MM-DD` (ignore `clearing_date`)
- `Payee`: take from `merchant_name`
- `Memo`: set to empty string
- `Amount`: take from `billing_amount` and force negative value

## Notes

- Keep CSV quoting enabled for safe import.
- Fail fast if required columns are missing.
- Preserve row order from the original export.
