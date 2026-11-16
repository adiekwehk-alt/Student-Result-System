# Student Result Management System

A menu-driven Python application for managing student records, scores, grades and reports.

## Features
- Add, view, search, update and delete students
- Record at least five subject scores per student, with date entered
- Total, average and grade (A-F) calculation, plus report cards
- Rank students by average or sort by name
- Class statistics (highest, lowest, class average)
- Save text reports to `reports/`
- Data stored in `data/students.json` (created automatically)

## Grading scale
| Average | Grade |
|---|---|
| 70+ | A |
| 60-69 | B |
| 50-59 | C |
| 45-49 | D |
| below 45 | F |

## How to run
Requires Python 3.8+ (standard library only).

```
python main.py
```

## Structure
```
main.py      menu and user interaction
student.py   Student class, regex ID and date validation
results.py   totals, averages, grading
storage.py   JSON load/save
reports.py   report card, tables, statistics, text export
data/        students.json
```

## Python concepts used
Variables and type conversion, if/elif/else, loops, lists/tuples/dicts, functions,
sorting with `sorted(key=...)`, try/except/else/finally, JSON file handling,
modules, OOP (`Student` class), `datetime`, `os`, `re` (regex validation).
