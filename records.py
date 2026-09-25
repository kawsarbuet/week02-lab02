# records.py
import json
from pathlib import Path
from datetime import datetime, date
import requests

SOURCE_URL = (
    "https://api.frankfurter.app/2024-01-01..2024-06-30"
    "?from=CAD&to=USD,EUR,GBP"
)

OUTPUT = Path("summary.json")


def fetch_records(url):
    """
    Download the records and return them as Python objects.
    Uses:
    - requests.get with timeout
    - raise_for_status()
    - clean exit on failure
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "rates" not in data:
            raise ValueError("Malformed API response: missing 'rates' field.")

        return data

    except Exception as exc:
        print(f"Download failed: {exc}")
        exit(1)


def parse_date(dstr):
    """Convert YYYY-MM-DD string to a date object."""
    return datetime.strptime(dstr, "%Y-%m-%d").date()


def filter_records(records, start_date, end_date):
    """
    Filter out:
    - dates before start_date (API includes last business day before)
    - malformed date strings
    - malformed rate maps
    """
    filtered = {}

    for dstr, rate_map in records.items():
        try:
            d = parse_date(dstr)
        except Exception:
            continue

        if not (start_date <= d <= end_date):
            continue

        if not isinstance(rate_map, dict):
            continue

        filtered[d] = rate_map

    return filtered


def monthly_average(records):
    """
    Compute monthly average rate per currency.
    Uses:
    - dictionary grouping
    - list comprehension
    - set comprehension
    """
    grouped = {}

    for d, rate_map in records.items():
        key = (d.year, d.month)
        grouped.setdefault(key, []).append(rate_map)

    monthly_avgs = {}

    for key, maps in grouped.items():
        currencies = {cur for m in maps for cur in m.keys()}

        avg_map = {}
        for cur in currencies:
            values = [m[cur] for m in maps if cur in m]
            if values:
                avg_map[cur] = sum(values) / len(values)

        # Convert month key to JSON-safe string
        month_key = f"{key[0]}-{key[1]:02d}"
        monthly_avgs[month_key] = avg_map

    return monthly_avgs


def largest_single_day_change(records):
    """
    Largest single-day change per currency.
    Uses:
    - sorted list of dates
    - dictionary for results
    """
    if not records:
        return {}

    dates = sorted(records.keys())
    currencies = {cur for r in records.values() for cur in r.keys()}

    result = {cur: {"change": 0.0, "from": None, "to": None} for cur in currencies}

    for i in range(1, len(dates)):
        prev_d = dates[i - 1]
        cur_d = dates[i]

        prev_rates = records[prev_d]
        cur_rates = records[cur_d]

        for cur in currencies:
            if cur in prev_rates and cur in cur_rates:
                change = abs(cur_rates[cur] - prev_rates[cur])
                if change > result[cur]["change"]:
                    result[cur] = {
                        "change": change,
                        "from": prev_d.isoformat(),  # FIXED
                        "to": cur_d.isoformat(),     # FIXED
                    }

    return result


def month_with_most_movement(records):
    """
    Month with highest total movement (sum of absolute daily changes).
    Uses:
    - dictionary grouping
    - set for currencies
    """
    if not records:
        return {}

    dates = sorted(records.keys())
    currencies = {cur for r in records.values() for cur in r.keys()}

    daily_changes = {d: {cur: 0.0 for cur in currencies} for d in dates}

    for i in range(1, len(dates)):
        prev_d = dates[i - 1]
        cur_d = dates[i]
        prev_rates = records[prev_d]
        cur_rates = records[cur_d]

        for cur in currencies:
            if cur in prev_rates and cur in cur_rates:
                daily_changes[cur_d][cur] = abs(cur_rates[cur] - prev_rates[cur])

    grouped = {}
    for d in dates:
        key = (d.year, d.month)
        grouped.setdefault(key, []).append(d)

    result = {}

    for cur in currencies:
        best_month = None
        best_total = 0.0

        for key, dlist in grouped.items():
            total = sum(daily_changes[d][cur] for d in dlist)
            if total > best_total:
                best_total = total
                best_month = key

        # Convert month key to JSON-safe string
        month_str = f"{best_month[0]}-{best_month[1]:02d}"

        result[cur] = {
            "month": month_str,
            "movement": best_total,
        }

    return result


def build_summary(records):
    """
    Combine the aggregations into one dict ready to write.
    """
    return {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
        "monthly_average": monthly_average(records),
        "largest_single_day_change": largest_single_day_change(records),
        "month_with_most_movement": month_with_most_movement(records),
    }


def write_summary(summary, path):
    """
    Write the summary to a JSON file using:
    - pathlib
    - encoding="utf-8"
    - indent=2
    """
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary written to {path}")


def main():
    """Main entry point."""
    raw = fetch_records(SOURCE_URL)

    start_date = date(2024, 1, 1)
    end_date = date(2024, 6, 30)

    records = filter_records(raw["rates"], start_date, end_date)

    if len(records) < 50:
        print("Error: fewer than 50 valid records after filtering.")
        exit(1)

    summary = build_summary(records)
    write_summary(summary, OUTPUT)


if __name__ == "__main__":
    main()
