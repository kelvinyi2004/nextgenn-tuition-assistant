import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env fallback
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TIMEZONE = os.getenv("TIMEZONE", "Asia/Kuala_Lumpur")
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))

# Roster configuration: defaults to roster.json if available, else roster.example.json
_custom_roster = Path(os.getenv("ROSTER_PATH", BASE_DIR / "config" / "roster.json"))
if _custom_roster.exists():
    ROSTER_FILE = _custom_roster
else:
    ROSTER_FILE = BASE_DIR / "config" / "roster.example.json"

DEFAULT_LESSONS_PER_MONTH = int(os.getenv("DEFAULT_LESSONS_PER_MONTH", "4"))
DEFAULT_LESSON_DURATION_MINUTES = int(os.getenv("DEFAULT_LESSON_DURATION_MINUTES", "60"))
ALLOW_CARRY_FORWARD = os.getenv("ALLOW_CARRY_FORWARD", "true").lower() in ("true", "1", "yes")
TRY_ORIGINAL_MONTH_FIRST = os.getenv("TRY_ORIGINAL_MONTH_FIRST", "true").lower() in ("true", "1", "yes")
