from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = BASE_DIR / "configs"

DATA_DIR = BASE_DIR / "data"

INPUT_DIR = DATA_DIR / "input"

OUTPUT_DIR = DATA_DIR / "output"

SESSION_DIR = BASE_DIR / "sessions"


ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".csv"}

MAX_FILE_SIZE_MB = 50


def ensure_directories():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)