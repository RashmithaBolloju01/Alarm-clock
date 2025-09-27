"""
alarms.alarm
Scheduling and management for alarms using threads and events.
"""
import threading
import uuid
from typing import Dict
import datetime
import time

from .utils import (
    speak,
    log_event,
    parse_time_str,
    seconds_until,
    get_current_time_str,
)

# Registry of scheduled alarms (alarm_id -> metadata)
ALARM_REGISTRY: Dict[str, dict] = {}

def validate_time_str(t: str) -> bool:
    """Return True if t is valid HH:MM:SS, else False."""
    try:
        parse_time_str(t)
        return True
    except Exception:
        return False

def schedule_alarm(alarm_time: str, label: str = "", snooze_minutes: int = 5) -> str:
    """
    Schedule an alarm. Returns alarm_id.
    The alarm runs in a background daemon thread and will prompt for snooze/dismiss when it fires.
    """
    alarm_id = str(uuid.uuid4())[:8]
    stop_event = threading.Event()
    thread = threading.Thread(
        target=_alarm_worker,
        args=(alarm_id, alarm_time, label, snooze_minutes, stop_event),
        daemon=True,
    )
    ALARM_REGISTRY[alarm_id] = {
        "id": alarm_id,
        "time": alarm_time,
        "label": label,
        "snooze_minutes": snooze_minutes,
        "thread": thread,
        "stop_event": stop_event,
        "status": "scheduled",
    }
    thread.start()
    log_event(f"Scheduled alarm {alarm_id} for {alarm_time} label='{label}' snooze={snooze_minutes}")
    return alarm_id

def cancel_alarm(alarm_id: str) -> bool:
    """Cancel a scheduled alarm. Returns True if cancelled."""
    record = ALARM_REGISTRY.get(alarm_id)
    if not record:
        return False
    record["stop_event"].set()
    record["status"] = "cancelled"
    log_event(f"Cancelled alarm {alarm_id}")
    return True

def list_alarms() -> list:
    """Return a list of alarm metadata (without thread/event objects)."""
    out = []
    for rec in ALARM_REGISTRY.values():
        out.append({
            "id": rec["id"],
            "time": rec["time"],
            "label": rec["label"],
            "snooze_minutes": rec["snooze_minutes"],
            "status": rec.get("status", "unknown"),
        })
    return out

def _alarm_worker(alarm_id: str, alarm_time: str, label: str, snooze_minutes: int, stop_event: threading.Event):
    """Background worker that sleeps until the alarm time, triggers, and optionally snoozes."""
    current_alarm_time = alarm_time
    while not stop_event.is_set():
        try:
            target_time = parse_time_str(current_alarm_time)
        except Exception as e:
            log_event(f"Alarm {alarm_id} has invalid time '{current_alarm_time}': {e}")
            ALARM_REGISTRY[alarm_id]["status"] = "error"
            return

        secs = seconds_until(target_time)
        # wait but respond early if cancelled
        stopped_early = stop_event.wait(timeout=secs)
        if stopped_early:
            # cancelled
            return

        # Trigger
        msg_label = label or alarm_id
        print(f"\n🔔 Alarm '{msg_label}' triggered (scheduled {current_alarm_time})")
        speak(f"Wake up. {label or 'Alarm'}")
        log_event(f"Alarm {alarm_id} triggered at scheduled {current_alarm_time}")
        ALARM_REGISTRY[alarm_id]["status"] = "triggered"

        # ask user whether to snooze
        try:
            choice = input(f"Alarm '{msg_label}': Snooze for {snooze_minutes} minutes? (y/n): ").strip().lower()
        except Exception:
            choice = "n"

        if choice == "y":
            # compute new time minutes from now
            new_dt = datetime.datetime.now() + datetime.timedelta(minutes=snooze_minutes)
            current_alarm_time = new_dt.time().strftime("%H:%M:%S")
            ALARM_REGISTRY[alarm_id]["time"] = current_alarm_time
            ALARM_REGISTRY[alarm_id]["status"] = "snoozed"
            log_event(f"Alarm {alarm_id} snoozed until {current_alarm_time}")
            # loop continues; worker will compute seconds_until(new_time)
            continue
        else:
            ALARM_REGISTRY[alarm_id]["status"] = "done"
            log_event(f"Alarm {alarm_id} dismissed by user")
            return
