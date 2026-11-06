# Student Academic Performance and Attendance Analytics Dashboard

This project is a Streamlit-based dashboard for analyzing student academic performance and attendance. It uses a realistic generated dataset with multiple classes, subjects, semesters, and student records.

## Project Features
- Overview of total students, average marks, average attendance, pass rate, and failures
- Subject-wise, class-wise, semester-wise, and grade-wise academic analysis
- Attendance trend and attendance vs performance scatter plots
- Student risk identification based on attendance and academic performance
- CSV upload for custom datasets
- Downloadable CSV reports for filtered data and summaries
- Beginner-friendly Python architecture

## Project Structure
```
student-academic-dashboard/
├── app.py
├── generate_dataset.py
├── student_performance.csv
├── requirements.txt
├── README.md
├── project_report.md
├── project_report.pdf
├── reports/
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
└── .gitkeep
```

## Requirements
Python 3.10+ is recommended.

## Installation
```bash
pip install -r requirements.txt
```

## Run the application
```bash
streamlit run app.py
```

## Regenerate the sample dataset
```bash
python generate_dataset.py
```

## Dataset Notes
The project includes a generated dataset with 150 students and 1,863 student-subject records across:
- 4 classes: BCA 1A, BCA 1B, BCA 2A, BCA 2B
- 6 subjects
- 6 semesters

## Dashboard Highlights
- Interactive filters for class, subject, semester, and grade
- KPI cards for academic monitoring
- Attendance analysis and risk segmentation
- Downloadable CSV reports based on the active filters
- CSV upload validation for invalid data and missing columns

## Report Files
- `project_report.md` contains the academic project report.
- `project_report.pdf` is generated when reportlab is available.

## Notes
The uploaded dataset is used only for the current application session, unless additional persistence is added by the developer.
