# CompareX

A config-driven Python reconciliation engine for comparing any two Excel datasets — inventory systems, financial data, ETL outputs, database exports, and more.

No code changes needed to add a new comparison job. Define the mapping once in YAML and run.

---

## Features

- Upload two Excel files via REST API (FastAPI + Swagger UI)
- Map mismatched column names between schemas
- Wildcard column matching (`Model Yield*`)
- Configurable join keys (single or composite)
- Float tolerance comparisons with named presets
- Value transformations before comparison (`x * 100`, `x.strip()`)
- Auto-detect and trim Excel footers
- Color-highlighted Excel diff report
- Summary sheet: matched/missing/extra rows + diff distributions
- Zero code changes to add new comparison jobs — just add a YAML config

---

## Quickstart

```bash
pip install -r requirements.txt
uvicorn comparex.main:app --reload
```

Open Swagger UI: `http://localhost:8000/docs`

**POST** `/api/reconcile` — upload two Excel files + select a config name → get back a downloadable diff report.

---

## How It Works

```
CONFIG (yaml)
    ↓
FILE LOADER  →  header row, file pattern
    ↓
NORMALIZER   →  lowercase + strip column names
    ↓
COLUMN MAPPER  →  rename to canonical names
    ↓
FOOTER TRIMMER  →  drop trailing rows
    ↓
VALIDATOR  →  ensure all expected columns present
    ↓
TRANSFORMS  →  apply per-column expressions
    ↓
TYPE CAST  →  string / float
    ↓
OUTER JOIN  →  on configured keys
    ↓
DIFF ENGINE  →  tolerance for floats, exact for strings
    ↓
REPORT  →  DETAIL sheet + SUMMARY sheet + color highlights
```

---

## Writing a Config

```yaml
job_name: inventory_reconciliation

datasets:
  left:
    name: wms
    file_pattern: wms_inventory*.xlsx
    header_row: 0
  right:
    name: erp
    file_pattern: erp_inventory*.xlsx
    header_row: 0

join:
  keys:
    - sku_code

column_mapping:
  sku_code:
    left: SKU Code
    right: SKU
  quantity:
    left: Qty on Hand
    right: Stock Qty
  unit_price:
    left: Unit Price
    right: Price

columns:
  sku_code:
    type: string
  quantity:
    type: float
    tolerance: 0
    highlight: true
    color: "#ffd6d6"
  unit_price:
    type: float
    tolerance: preset_price
    highlight: true
    color: "#fff2cc"

tolerance_presets:
  preset_price:
    abs: 0.01

output:
  file_name: inventory_diff.xlsx

options:
  case_insensitive_strings: true
  trim_strings: true
```

See `src/configs/` for more examples including financial reconciliation use cases.

---

## Column Config Options

| Field | Description |
|-------|-------------|
| `type` | `float` or `string` |
| `tolerance` | absolute threshold (float) or named preset |
| `transform` | eval expression applied before comparison (`left`/`right`) |
| `highlight` | highlight mismatches in Excel output |
| `color` | hex color for highlights |
| `label` | display name in report columns |
| `ignore` | skip this column in diff |
| `summary` | include diff distribution in SUMMARY sheet |

---

## Use Cases

- **Inventory**: WMS vs ERP stock counts
- **Finance**: Two data vendor outputs (prices, yields, ratings)
- **ETL validation**: source vs destination after a pipeline run
- **Data migration**: pre/post record comparison
- **Audit**: any two structured tabular exports

---

## Project Structure

```
src/
  comparex/
    main.py              # FastAPI app
    api.py               # upload/download endpoints
    reconcile_service.py # core pipeline
    config_loader.py     # YAML loader
  configs/
    example-inventory.yaml   # generic example
    fimmda-slv.yaml          # financial reconciliation example
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/configs` | list available configs |
| `POST` | `/api/reconcile` | upload files + run comparison |
| `GET` | `/api/download/{run_id}` | download diff report |
| `DELETE` | `/api/clear` | clear input/output files |
| `POST` | `/reconcile/{config_name}` | run from files already in `data/input/` |

---

## Tech Stack

- **Python 3.11+**
- **FastAPI** — REST API
- **pandas** — data processing
- **openpyxl** — Excel read/write + highlighting
- **PyYAML** — config parsing
- **uv** — dependency management
