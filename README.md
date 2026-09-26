# AIGC 5005 — Lab 02 — Aggregating Records

This project downloads foreign exchange rate records from the Frankfurter API, filters them, computes multiple aggregations, and writes a summary to a JSON file.  
The program follows the required structure from the assignment: each function performs one job, aggregation functions do not download or write data, and the entry point is protected by the main guard.

---

## 📌 Source

The program retrieves exchange rates for CAD → USD, EUR, GBP over the date range:

**2024‑01‑01 to 2024‑06‑30**

## API endpoint: 
https://api.frankfurter.app/2024-01-01..2024-06-30?from=CAD&to=USD,EUR,GBP


The API omits weekends and holidays and may include the last business day before the start date.  
The program filters these out.

---

## 📁 Files

- `records.py` — main program
- `summary.json` — generated output file

---

## 🧩 Program Structure

The program is organized into the following functions:

### `fetch_records(url)`
Downloads records using:
- `requests.get`  
- `timeout=10`  
- `raise_for_status()`  

Exits cleanly with a message if the download fails.

### `filter_records(records, start_date, end_date)`
Filters:
- dates before the start date  
- malformed date strings  
- malformed rate maps  

Returns only valid records.

### Aggregation Functions  
Each aggregation takes records **in** and returns a result.  
None of them download, print, or write anything.

#### `monthly_average(records)`
Computes monthly average exchange rates per currency.  
Uses:
- dictionary grouping  
- list comprehension  
- set comprehension  

#### `largest_single_day_change(records)`
Finds the largest single‑day change per currency.  
Uses:
- sorted list of dates  
- dictionary for results  

#### `month_with_most_movement(records)`
Finds the month with the highest total movement (sum of absolute daily changes).  
Uses:
- dictionary grouping  
- set for currencies  

### `build_summary(records)`
Combines all aggregations into one dictionary ready to write.

### `write_summary(summary, path)`
Writes the summary to a JSON file using:
- `pathlib.Path.write_text`
- `encoding="utf-8"`
- `indent=2`

### `main()`
Coordinates:
1. Download  
2. Filter  
3. Aggregate  
4. Write summary  

Protected by the main guard.

---

## 📊 Collections Used (Required)

The program uses **three** collection types, each for a justified purpose:

- **Dictionary** — grouping records by month, storing rate maps, building summary  
- **List** — storing daily rate maps within each month  
- **Set** — collecting unique currencies from records  

---

## 🧪 Error Handling

The program handles:
- network errors  
- malformed dates  
- malformed rate maps  
- missing fields  
- insufficient records (<50)  

All errors produce clear messages instead of tracebacks.

---

## 📦 Output

The generated `summary.json` includes:

- source URL  
- number of records processed  
- monthly averages  
- largest single‑day changes  
- month with most movement  

All dates and month keys are converted to JSON‑safe strings.

---

## ▶️ Running the Program

## Step-1: Create and activate a virtual environment:

From the terminal:
mkdir week02-lab02
cd week02-lab02

python -m venv .venv

# macOS and Linux 
source .venv/bin/activate 
# Windows PowerShell 
.venv\Scripts\Activate.ps1 
# Windows Command Prompt 
.venv\Scripts\activate.bat

## Step-2: Install packages from requirements.txt file

pip install -r requirements.txt

## Step-3: Run the program file records.py
python records.py


## Example output ////summary.json file

{
  "source_url": "https://api.frankfurter.app/2024-01-01..2024-06-30?from=CAD&to=USD,EUR,GBP",
  "records_processed": 125,
  "monthly_average": {
    "2024-01": {"USD": 0.75, "EUR": 0.68, "GBP": 0.59},
    "2024-02": {"USD": 0.74, "EUR": 0.67, "GBP": 0.58}
  },
  "largest_single_day_change": {
    "USD": {"change": 0.012, "from": "2024-03-04", "to": "2024-03-05"}
  }
}

## What this tells about:

The program successfully downloaded and filtered more than 50 valid records.
Monthly averages show how CAD fluctuated against USD, EUR, and GBP over time.
The largest single‑day change highlights the most volatile day for each currency.
All dates are converted to ISO strings, confirming correct JSON serialization.

## Data quirks: 
The Frankfurter API contains several quirks that the program must handle:

## Missing dates
The API does not return weekends or holidays.
Program response:  
The code processes only the dates provided, without assuming continuity.

## Pre‑start business day included
Queries like 2024‑01‑01..2024‑06‑30 may include the last business day of 2023.
Program response:  
filter_records() removes any date earlier than the start date.

## Malformed or incomplete rate maps
Some entries may be missing currencies or contain unexpected structures.
Program response:  
The program checks isinstance(rate_map, dict) and skips malformed entries.

## Python date objects cannot be serialized to JSON
JSON cannot encode date objects directly.
Program response:  
All dates are converted using .isoformat() before writing the summary.

## Design choices: 
The program uses three core collection types, each chosen for a specific purpose:

1. Dictionary (dict)
Used for grouping records by month, storing rate maps, and building the final summary.
Reason:  
Dictionaries provide fast lookups and a natural key→value structure for dates, months, and currency mappings.

2. List (list)
Used for storing daily rate maps within each month and iterating through sorted dates.
Reason:  
Lists preserve order and allow efficient iteration when computing averages or daily changes.

3. Set (set)
Used for collecting unique currencies across all records.
Reason:  
Sets automatically remove duplicates and ensure each currency is processed exactly once.

4. Comprehensions
List and set comprehensions make aggregation code concise, readable, and efficient.

## Known limitations:
Missing currency values within a month
If a currency appears only on some days, the monthly average is computed only from available values.
A more advanced version could interpolate or normalize missing data.

## 1. Hard‑coded date range and URL
The program does not accept command‑line arguments.
Future improvements could allow custom date ranges, currencies, or output paths.

## 2. No visualization
The output is JSON only.
Charts or graphs could make trends easier to interpret.

## 3. No unit tests yet
The program is structured well for testing, but tests are not included.
This will likely be required in Week 4.

## 4.Assumes API availability
If the API changes or becomes unavailable, the program exits cleanly but does not retry or cache data.

