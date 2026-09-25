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



