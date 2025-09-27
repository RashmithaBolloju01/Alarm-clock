"""
CLI entry point for the alarm clock project.
"""
from alarms.alarm import schedule_alarm, list_alarms, cancel_alarm, validate_time_str
from alarms.utils import ensure_data_dirs, get_current_time_str, load_sample_alarms
import time
import sys

def print_menu() -> None:
    print("\n=== ALARM CLOCK MENU ===")
    print("1. Set a new alarm")
    print("2. View scheduled alarms")
    print("3. Cancel an alarm")
    print("4. View alarm log (last lines)")
    print("5. Exit")

def tail_log(lines: int = 20):
    try:
        with open("alarm_log.txt", "r", encoding="utf-8") as f:
            content = f.readlines()
            for line in content[-lines:]:
                print(line.rstrip())
    except FileNotFoundError:
        print("No log file yet (no alarms fired).")

def main():
    ensure_data_dirs()
    print("Alarm Clock — macOS version")
    # load optional sample alarms (informational only)
    samples = load_sample_alarms()
    if samples:
        print(f"Loaded {len(samples)} sample alarms from data/sample_alarms.json")

    while True:
        print_menu()
        choice = input("Choose (1-5): ").strip()
        if choice == "1":
            t = input("Enter alarm time (HH:MM:SS, 24-hour): ").strip()
            if not validate_time_str(t):
                print("Invalid time format. Try again.")
                continue
            label = input("Label (optional): ").strip()
            snooze = input("Snooze minutes (default 5): ").strip()
            try:
                snooze_min = int(snooze) if snooze else 5
            except ValueError:
                snooze_min = 5
            alarm_id = schedule_alarm(t, label=label, snooze_minutes=snooze_min)
            print(f"Scheduled alarm id={alarm_id} at {t} (snooze {snooze_min}m).")
        elif choice == "2":
            alarms = list_alarms()
            if not alarms:
                print("No alarms scheduled.")
            else:
                print("Scheduled alarms:")
                for a in alarms:
                    print(f" - id={a['id']} time={a['time']} label='{a['label']}' snooze={a['snooze_minutes']} status={a['status']}")
        elif choice == "3":
            aid = input("Enter alarm id to cancel: ").strip()
            ok = cancel_alarm(aid)
            print("Cancelled." if ok else "No alarm with that id.")
        elif choice == "4":
            tail_log(30)
        elif choice == "5":
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
