"""
alarms.utils
Helper functions: speak, logging, time parsing and calculations.
"""
from pathlib import Path
import datetime
import os
import json
from typing import List

ROOT = Path(__file__).parents[1]
LOG_FILE = ROOT / "alarm_log.txt"
DATA_DIR = ROOT / "data"
SAMPLE_FILE = DATA_DIR / "sample_alarms.json"

def ensure_data_dirs() -> None:
    """Create data/ directory if missing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def speak(message: str) -> None:
    """macOS voice output (uses 'say')."""
    # Keep call simple and safe — no shell injection expected since message is local.
    os.system(f"say '{message}'")

def log_event(message: str) -> None:
    """Append a timestamped line to alarm_log.txt."""
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat()} - {message}\n")

def get_current_time_str() -> str:
    """Return current time as HH:MM:SS."""
    return datetime.datetime.now().strftime("%H:%M:%S")

def parse_time_str(t: str) -> datetime.time:
    """Parse HH:MM:SS string to datetime.time (raises ValueError on bad format)."""
    return datetime.datetime.strptime(t, "%H:%M:%S").time()

def seconds_until(target_time: datetime.time) -> int:
    """Return seconds until the next occurrence of target_time (today or tomorrow)."""
    now = datetime.datetime.now()
    target_dt = datetime.datetime.combine(now.date(), target_time)
    if target_dt <= now:
        target_dt += datetime.timedelta(days=1)
    return int((target_dt - now).total_seconds())

def load_sample_alarms() -> List[dict]:
    """Load data/sample_alarms.json if present."""
    ensure_data_dirs()
    if SAMPLE_FILE.exists():
        with SAMPLE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_sample_alarms(alarms: List[dict]) -> None:
    """Write sample_alarms.json (overwrites)."""
    ensure_data_dirs()
    with SAMPLE_FILE.open("w", encoding="utf-8") as f:
        json.dump(alarms, f, indent=2)
