import random
from pathlib import Path

import pandas as pd

OUTPUT_FILE = Path(__file__).resolve().parent / "student_performance.csv"

CLASSES = ["BCA 1A", "BCA 1B", "BCA 2A", "BCA 2B"]
SUBJECTS = [
    "Python Programming",
    "Mathematics",
    "Database Management Systems",
    "Computer Networks",
    "Web Development",
    "Operating Systems",
]
SEMESTERS = [1, 2, 3, 4, 5, 6]
FIRST_NAMES = [
    "Aarav", "Aisha", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Mihir",
    "Neha", "Rahul", "Sanya", "Ved", "Prerna", "Rohan", "Tanvi", "Yash", "Zoya",
    "Nisha", "Harsh", "Meera", "Aditya", "Pooja", "Vikram", "Sakshi", "Manav",
]
LAST_NAMES = [
    "Sharma", "Patel", "Verma", "Singh", "Kapoor", "Nair", "Reddy", "Iyer",
    "Joshi", "Malhotra", "Khan", "Gupta", "Chauhan", "Rao", "Saxena", "Mishra",
    "Dutta", "Sen", "Bose", "Mehta", "Kulkarni", "Agarwal", "Pandey", "Thomas",
]


def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def get_grade(marks_percentage):
    if marks_percentage >= 90:
        return "A"
    if marks_percentage >= 80:
        return "B"
    if marks_percentage >= 70:
        return "C"
    if marks_percentage >= 60:
        return "D"
    if marks_percentage >= 40:
        return "E"
    return "F"


def generate_record(student_id, student_name, class_name, semester, subject, profile):
    if profile == "high":
        marks_percentage = random.randint(78, 98)
        attendance = random.randint(78, 98)
    elif profile == "average":
        marks_percentage = random.randint(52, 82)
        attendance = random.randint(62, 90)
    else:
        marks_percentage = random.randint(28, 62)
        attendance = random.randint(35, 80)

    total_marks = random.choice([100, 120])
    marks_obtained = round((marks_percentage / 100) * total_marks, 2)
    attendance = min(100, max(0, attendance))
    marks_obtained = min(total_marks, max(0, marks_obtained))
    grade = get_grade(marks_percentage)
    result = "Pass" if marks_percentage >= 40 else "Fail"

    return {
        "Student_ID": student_id,
        "Student_Name": student_name,
        "Class": class_name,
        "Subject": subject,
        "Semester": semester,
        "Marks_Obtained": round(marks_obtained, 2),
        "Total_Marks": total_marks,
        "Attendance_Percentage": attendance,
        "Grade": grade,
        "Result": result,
    }


def generate_dataset(total_students=150):
    random.seed(42)
    records = []

    for student_number in range(1, total_students + 1):
        student_id = f"STU-{student_number:04d}"
        student_name = generate_name()
        class_name = random.choice(CLASSES)
        profile = random.choices(["high", "average", "low"], weights=[0.32, 0.45, 0.23], k=1)[0]
        semesters = random.sample(SEMESTERS, random.randint(2, 4))
        semesters.sort()

        for semester in semesters:
            subject_pool = random.sample(SUBJECTS, random.randint(3, 5))
            for subject in subject_pool:
                records.append(
                    generate_record(student_id, student_name, class_name, semester, subject, profile)
                )

    df = pd.DataFrame(records)
    df.columns = [
        "Student_ID",
        "Student_Name",
        "Class",
        "Subject",
        "Semester",
        "Marks_Obtained",
        "Total_Marks",
        "Attendance_Percentage",
        "Grade",
        "Result",
    ]
    return df


if __name__ == "__main__":
    data = generate_dataset()
    data.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset created successfully at {OUTPUT_FILE} with {len(data)} records.")
