"""Score calculation and grading logic."""

MIN_SUBJECTS = 5
GRADE_BANDS = [(70, "A"), (60, "B"), (50, "C"), (45, "D")]  # below 45 -> F


def calculate_total(student):
    return sum(student.scores.values())


def calculate_average(student):
    """Average of all recorded scores (0 if none)."""
    if not student.scores:
        return 0.0
    return calculate_total(student) / len(student.scores)


def assign_grade(average):
    for minimum, grade in GRADE_BANDS:
        if average >= minimum:
            return grade
    return "F"


def has_complete_results(student):
    return len(student.scores) >= MIN_SUBJECTS


def summary(student):
    """Return (total, average, grade) as a tuple."""
    avg = calculate_average(student)
    return calculate_total(student), avg, assign_grade(avg)
