"""Report generation functions."""
import os
from datetime import datetime
import results


def report_card(student):
    total, avg, grade = results.summary(student)
    lines = ["=" * 44, f"REPORT CARD - {student.name}",
             f"ID: {student.student_id}   Class: {student.form}   Gender: {student.gender}",
             f"Date of birth: {student.dob}", "-" * 44]
    if not student.scores:
        lines.append("No scores recorded yet.")
    for subject, score in student.scores.items():
        lines.append(f"{subject:<25}{score:>8.1f}")
    lines += ["-" * 44, f"Total:   {total:.1f}", f"Average: {avg:.2f}", f"Grade:   {grade}",
              f"Results entered: {student.date_entered or 'N/A'}", "=" * 44]
    return "\n".join(lines)


def sorted_students(students, by="average"):
    """Sort by average (high to low) or by name (A-Z)."""
    items = list(students.values())
    if by == "name":
        return sorted(items, key=lambda s: s.name.lower())
    return sorted(items, key=results.calculate_average, reverse=True)


def results_table(student_list):
    lines = [f"{'#':<4}{'ID':<10}{'Name':<25}{'Total':>8}{'Average':>9}{'Grade':>7}", "-" * 63]
    for i, s in enumerate(student_list, 1):
        total, avg, grade = results.summary(s)
        lines.append(f"{i:<4}{s.student_id:<10}{s.name:<25}{total:>8.1f}{avg:>9.2f}{grade:>7}")
    return "\n".join(lines)


def class_statistics(students):
    """Return dict of stats, or None if no scored students."""
    scored = [s for s in students.values() if s.scores]
    if not scored:
        return None
    all_scores = [v for s in scored for v in s.scores.values()]
    averages = [results.calculate_average(s) for s in scored]
    return {
        "students": len(scored),
        "highest_score": max(all_scores),
        "lowest_score": min(all_scores),
        "class_average": sum(averages) / len(averages),
        "top_student": max(scored, key=results.calculate_average).name,
    }


def statistics_text(students):
    st = class_statistics(students)
    if st is None:
        return "No scores available for statistics."
    return (f"Students with scores: {st['students']}\n"
            f"Highest score:  {st['highest_score']:.1f}\n"
            f"Lowest score:   {st['lowest_score']:.1f}\n"
            f"Class average:  {st['class_average']:.2f}\n"
            f"Top student:    {st['top_student']}")


def save_text_report(students, folder="reports"):
    """Save a full class report to a timestamped text file; return its path."""
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"class_report_{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"CLASS RESULT REPORT - generated {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write(results_table(sorted_students(students)) + "\n\n")
        f.write("CLASS STATISTICS\n" + statistics_text(students) + "\n")
    return path
