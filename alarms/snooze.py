"""
alarms.snooze
Small helper to compute new alarm times when snoozing.
"""
from datetime import datetime, timedelta

def compute_snoozed_time_from_now(minutes: int = 5) -> str:
    """Return time string HH:MM:SS minutes from now."""
    new_dt = datetime.now() + timedelta(minutes=minutes)
    return new_dt.time().strftime("%H:%M:%S")
