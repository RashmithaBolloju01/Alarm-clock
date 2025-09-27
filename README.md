# Alarm Clock

**Alarm Clock** is a Python-based desktop application that allows users to set, manage, and snooze alarms with a simple command-line interface. Designed for clarity and modularity, it demonstrates Python best practices such as package structuring, reusable utilities, and logging — making it both beginner-friendly and extensible for more advanced features like GUI or notifications.

## Project Overview

This project focuses on creating a **fully functional alarm system** in Python. It emphasizes modular code organization, practical time scheduling, and logging for user interactions. While currently running on a command-line interface, the structure allows smooth expansion into GUI-based applications or even integration with web backends.

## Features

* Set alarms with custom time and labels
* Snooze functionality to delay alarms
* Alarm dismiss option
* Automatic logging of all actions (`alarm_log.txt`)
* Modular package design (`alarms/` folder with separate files for logic, utils, snooze)
* Extendable to support sound, voice alerts, or desktop notifications

## Technologies Used

| Category      | Tools & Libraries                          |
| ------------- | ------------------------------------------ |
| Language      | Python 3 (cross-platform, tested on macOS) |
| Standard Libs | `datetime`, `time`, `threading`, `pathlib` |
| Optional      | `say` (macOS command for voice alerts)     |

## Project Structure

```
alarm-clock/
├── alarms/
│   ├── __init__.py       # Marks folder as a Python package
│   ├── alarm.py          # Core alarm logic (set & trigger)
│   ├── snooze.py         # Snooze functionality
│   └── utils.py          # Helpers: logging, speaking, formatting
│
├── data/
│   └── sample_alarms.json  # Example alarm data (optional)
│
├── docs/
│   ├── project_plan.md     # Planned features, improvements
│   └── usage.md            # Extended usage instructions
│
├── tests/
│   └── test_alarm.py       # Unit tests for alarm logic
│
├── main.py                 # CLI entry point
├── requirements.txt        # Dependencies (pytest, etc.)
├── .gitignore              # Ignore logs, cache, env
└── README.md               # Project documentation
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/<your-username>/alarm-clock.git
cd alarm-clock
```

(Recommended) Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies (if any):

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python3 main.py
```

## Sample Use Case

1. The user runs the program and selects **“Set a new alarm”**.
2. They enter the time (e.g., `07:30`) and a label (`Morning Study`).
3. The alarm is scheduled. At the set time, the alarm triggers:

   * The system speaks the label (on macOS).
   * The event is logged in `alarm_log.txt`.
4. The user chooses to **snooze** or **dismiss**.

## Future Enhancements

* GUI with **Tkinter** or **PyQt**
* Cross-platform sound notifications
* Save/load recurring alarms in JSON or SQLite
* Integration with Google Calendar or reminders
* Mobile/desktop push notifications

## License

This project is licensed under the **MIT License**.
