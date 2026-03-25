# Excel Recon Engine

A config-driven Python reconciliation engine for comparing Excel datasets such as **FIMMDA vs 3Cortex**, **NSDL vs Internal**, or any structured tabular data.

The system is designed for **deterministic, repeatable, and scalable data comparison**, with minimal UI dependency. It runs via **FastAPI (Swagger)** and can later be extended with UI or automation layers.

---

# Key Capabilities

- Upload or drop Excel files into a folder
- Select comparison logic via config (YAML)
- Map columns between different schemas
- Normalize column names automatically
- Define join keys (eg: ISIN)
- Support string and numeric comparisons
- Configure tolerance rules
- Apply transformation rules (eg: multiply by 100)
- Generate mismatch-only Excel report
- Designed for reuse across multiple reconciliation problems

---

# Primary Use Case

Example:

Compare:

FIMMDA SLV vs 3Cortex SLV

Differences handled:

- Coupon 7.25 vs 0.0725
- Column names differ
- Floating point precision mismatch
- Extra rows in one dataset
- Case differences in issuer names

---

# System Architecture

Pipeline:

CONFIG (yaml)
    ↓
FILE LOADER
    ↓
HEADER HANDLING
    ↓
COLUMN NORMALIZATION
    ↓
COLUMN MAPPING
    ↓
COLUMN VALIDATION
    ↓
TRANSFORMATION RULES
    ↓
TYPE CASTING
    ↓
JOIN ENGINE
    ↓
DIFF ENGINE
    ↓
REPORT GENERATOR

---

# Project Structure

excel_recon/

app/
    main.py
    reconcile_service.py
    config_loader.py

configs/
    fimmda_slv.yaml

data/
    input/
    output/

requirements.txt

---

# Installation

Create virtual environment:

pip install -r requirements.txt

requirements.txt:

fastapi
uvicorn
pandas
openpyxl
pyyaml
numpy
python-multipart

---

# Running the API

Start server:

uvicorn app.main:app --reload

Swagger UI:

http://localhost:8000/docs

---

# How to Run Reconciliation

Step 1:

Place files in:

data/input/

Example:

data/input/fimmda_20260326.xlsx
data/input/3cortex_20260326.xlsx

Step 2:

Call API from Swagger:

POST /reconcile/fimmda_slv

Response:

{
  "status": "success",
  "rows": 23,
  "output": "data/output/fimmda_slv_diff.xlsx"
}

Step 3:

Open output file:

data/output/fimmda_slv_diff.xlsx

---

# Configuration File

configs/fimmda_slv.yaml

Controls entire comparison logic.

Example:

job_name: fimmda_slv_compare

datasets:

  left:
    name: fimmda
    file_pattern: fimmda*.xlsx
    header_row: 2

  right:
    name: 3cortex
    file_pattern: 3cortex*.xlsx
    header_row: 1


join:

  keys:
    - isin


column_mapping:

  isin:
    left: ISIN
    right: isin

  coupon:
    left: Coupon Rate
    right: coupon_rate


columns:

  isin:
    type: string

  coupon:
    type: float
    tolerance: 0.0001
    transform:
      right: "x * 100"


tolerance_presets:

  preset_price:
    abs: 0.01

  preset_yield:
    abs: 0.0001


output:

  file_name: fimmda_slv_diff.xlsx


options:

  case_insensitive_strings: true
  trim_strings: true

---

# Configuration Specification

datasets

Defines file names and header rows.

left / right

Logical dataset names used in output column naming.

Example output columns:

coupon_fimmda
coupon_3cortex

file_pattern

Pattern used to pick file automatically.

Example:

fimmda*.xlsx

header_row

Row index containing column names.

0 based index.

Example:

header_row: 2

means 3rd row contains headers.

---

# Join Keys

join:

  keys:
    - isin

Supports multiple keys:

  keys:
    - isin
    - maturity_date

Join type:

outer join (ensures missing rows are captured)

---

# Column Mapping

Maps real Excel column names to canonical internal column names.

Example:

column_mapping:

  coupon:
    left: Coupon Rate
    right: coupon_rate

Internal canonical column:

coupon

Allows different Excel schemas to be compared.

---

# Column Definitions

columns:

Defines comparison logic per column.

Example:

coupon:

  type: float

  tolerance: 0.0001

  transform:

    right: "x * 100"

Supported types:

string
float

---

# Transformation Rules

Allows value transformation before comparison.

Example:

3cortex coupon = 0.0725
FIMMDA coupon = 7.25

Transform:

transform:

  right: "x * 100"

Expression variable:

x = original value

Examples:

"x * 100"

"x / 100"

"x.replace(',', '')"

"round(x,4)"

---

# Tolerance Rules

Floating point comparisons use tolerance.

Example:

tolerance: 0.01

Means:

100.01 vs 100.02 = equal

Supports presets:

tolerance: preset_yield

Define presets:

tolerance_presets:

  preset_yield:

    abs: 0.0001

  preset_price:

    abs: 0.01

---

# Header Row Selection

Different files may have headers at different positions.

Example:

left:

  header_row: 2

Means:

Excel row 3 contains column names.

Implemented via:

pandas.read_excel(header=2)

---

# Column Validation

Engine validates:

All configured columns exist in both datasets.

Example error:

Missing columns in LEFT file:
['coupon']

Prevents silent comparison failures.

---

# Output Format

Output contains:

Only mismatched rows.

Columns:

key columns

value from left dataset

value from right dataset

diff flag per column

Example:

isin
coupon_fimmda
coupon_3cortex
coupon_diff
vwap_fimmda
vwap_3cortex
vwap_diff

---

# Output Example

| isin | coupon_fimmda | coupon_3cortex | coupon_diff |
|------|--------------|----------------|------------|
| INE123 | 7.25 | 7.24 | TRUE |

---

# Internal Code Explanation

main.py

FastAPI entry point.

Exposes endpoint:

POST /reconcile/{config_name}

---

config_loader.py

Loads YAML configuration.

Validates config exists.

---

reconcile_service.py

Core engine.

Functions:

load_dataset

Loads Excel file based on pattern and header row.

normalize

Standardizes column names.

lowercase
strip spaces
replace spaces with underscore

map_columns

Maps Excel column names to canonical column names.

Example:

Coupon Rate → coupon

validate_columns

Checks configured columns exist in both datasets.

apply_transforms

Applies transformation rules before comparison.

cast_types

Converts column types.

string
float

resolve_tolerance

Resolves tolerance numeric value or preset.

join_data

Performs outer join on keys.

compare_data

Performs comparison logic.

float → tolerance comparison

string → case insensitive comparison

build_report

Exports Excel output.

---

# Error Handling

Engine raises errors when:

file not found

missing column mapping

missing tolerance preset

invalid transform expression

invalid header row

---

# Extending the Engine

Add new comparison:

create new config file.

configs/nsdl_positions.yaml

No code changes required.

---

# Future Enhancements (Planned)

UI for config creation

column auto-detection

date normalization

summary sheet

multi-sheet support

scheduled runs

config database storage

diff statistics

---

# Summary

This engine provides:

reusable comparison logic

config driven behavior

consistent outputs

minimal manual effort

production scalable structure

Suitable for:

financial reconciliation

ETL validation

data migration verification

audit comparisons

quality checks

---