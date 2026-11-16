"""Load and save data (JSON)."""
import json
import os
from student import Student

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students(path=DATA_FILE):
    """Load students into a dict {id: Student}. Missing/corrupt file -> empty."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print("No data file found. Starting with an empty database.")
        return {}
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting empty.")
        return {}
    else:
        return {d["student_id"]: Student.from_dict(d) for d in raw}


def save_students(students, path=DATA_FILE):
    """Write all students to the JSON file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=4)
    except OSError as err:
        print(f"Error saving data: {err}")
        return False
    return True
