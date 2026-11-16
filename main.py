"""Student Result Management System - entry point and menu."""
import storage
import results
import reports
from student import Student, is_valid_id, is_valid_date

GENDERS = {"M": "Male", "F": "Female"}


def ask(prompt):
    return input(prompt).strip()


def ask_nonempty(prompt):
    while True:
        value = ask(prompt)
        if value:
            return value
        print("This field cannot be empty.")


def ask_score(subject):
    while True:
        try:
            score = float(ask(f"  {subject} score (0-100): "))
        except ValueError:
            print("  Please enter a number.")
            continue
        if 0 <= score <= 100:
            return score
        print("  Score must be between 0 and 100.")


def find_student(students):
    sid = ask("Enter Student ID: ").upper()
    student = students.get(sid)
    if student is None:
        print("Student not found.")
    return student


def add_student(students):
    while True:
        sid = ask("Student ID (e.g. STU001): ").upper()
        if not is_valid_id(sid):
            print("Invalid ID format. Use letters followed by digits, e.g. STU001.")
        elif sid in students:
            print("That ID already exists.")
        else:
            break
    name = ask_nonempty("Full name: ").title()
    form = ask_nonempty("Class/Form: ")
    while True:
        g = ask("Gender (M/F): ").upper()
        if g in GENDERS:
            break
        print("Enter M or F.")
    while True:
        dob = ask("Date of birth (YYYY-MM-DD): ")
        if is_valid_date(dob):
            break
        print("Invalid date.")
    students[sid] = Student(sid, name, form, GENDERS[g], dob)
    print(f"Student {name} added.")


def view_all(students):
    if not students:
        print("No students registered.")
        return
    for s in students.values():
        print(s)


def search_student(students):
    term = ask("Search by ID or name: ").lower()
    matches = [s for s in students.values()
               if term == s.student_id.lower() or term in s.name.lower()]
    if not matches:
        print("No match found.")
    for s in matches:
        print(s)


def update_student(students):
    s = find_student(students)
    if not s:
        return
    print("Leave blank to keep the current value.")
    s.name = ask(f"Name [{s.name}]: ").title() or s.name
    s.form = ask(f"Class [{s.form}]: ") or s.form
    g = ask(f"Gender M/F [{s.gender}]: ").upper()
    if g in GENDERS:
        s.gender = GENDERS[g]
    dob = ask(f"DOB [{s.dob}]: ")
    if dob and is_valid_date(dob):
        s.dob = dob
    elif dob:
        print("Invalid date; DOB unchanged.")
    print("Student updated.")


def delete_student(students):
    s = find_student(students)
    if s and ask(f"Delete {s.name}? (y/n): ").lower() == "y":
        del students[s.student_id]
        print("Student deleted.")


def record_scores(students):
    s = find_student(students)
    if not s:
        return
    if s.scores:
        print("Existing scores:", s.scores)
    while True:
        subject = ask("Subject name (blank to finish): ").title()
        if not subject:
            break
        s.set_score(subject, ask_score(subject))
    if not results.has_complete_results(s):
        print(f"Note: at least {results.MIN_SUBJECTS} subjects are required "
              f"(currently {len(s.scores)}).")


def show_report_card(students):
    s = find_student(students)
    if s:
        print(reports.report_card(s))


def show_ranking(students):
    if not students:
        print("No students registered.")
        return
    choice = ask("Sort by (1) average or (2) name: ")
    by = "name" if choice == "2" else "average"
    print(reports.results_table(reports.sorted_students(students, by)))


def show_statistics(students):
    print(reports.statistics_text(students))


def export_report(students):
    if not students:
        print("No students to report on.")
        return
    try:
        path = reports.save_text_report(students)
        print(f"Report saved to {path}")
    except OSError as err:
        print(f"Could not save report: {err}")


MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student            7. Show report card
 2. View all students      8. Results list / ranking
 3. Search student         9. Class statistics
 4. Update student        10. Save text report
 5. Delete student         0. Save and exit
 6. Record/update scores
"""

ACTIONS = {
    "1": add_student, "2": view_all, "3": search_student, "4": update_student,
    "5": delete_student, "6": record_scores, "7": show_report_card,
    "8": show_ranking, "9": show_statistics, "10": export_report,
}


def main():
    students = storage.load_students()
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            if storage.save_students(students):
                print("Data saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option.")
            continue
        try:
            action(students)
            storage.save_students(students)   # auto-save after every action
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
        except Exception as err:               # last-resort safety net
            print(f"Unexpected error: {err}")
        finally:
            pass


if __name__ == "__main__":
    main()
