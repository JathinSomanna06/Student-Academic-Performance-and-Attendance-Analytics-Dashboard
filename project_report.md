# Student Academic Performance and Attendance Analytics Dashboard

Student Name: [Student Name]
Registration Number: [Registration Number]
College: [College Name]
Department: [Department Name]
Submission Date: [DD/MM/YYYY]

## 1. Abstract
This project presents a professional and interactive dashboard developed using Python and Streamlit to analyze student academic performance and attendance. The system helps teachers and academic administrators monitor subject performance, identify low-performing and at-risk students, and understand trends across classes and semesters. The application loads a realistic generated dataset, supports filtering, and enables CSV uploads for custom analysis. The dashboard combines KPI cards, charts, summary tables, and downloadable reports to make academic decision-making easier.

## 2. Introduction
Educational institutions often deal with large volumes of academic and attendance data. Manually reviewing records is time-consuming and error-prone. A digital dashboard can simplify this by presenting performance trends and highlighting students who need support. This project fills that need by creating an academic analytics dashboard that is easy to run and understand, even for beginners.

## 3. Problem Statement
Teachers need a quick and effective way to review the performance of students across multiple subjects, semesters, classes, and attendance levels. Without a dashboard, identifying weak students, struggling classes, and low-attendance records becomes difficult. There is also a need to analyze performance and attendance together when deciding whether a student requires academic mentoring or attendance action.

## 4. Project Objectives
The primary objectives of the project are to:
- Build an interactive dashboard using Streamlit
- Provide performance analysis by subject, class, grade, and semester
- Analyze attendance patterns and their relationship with marks
- Identify at-risk students using transparent rules
- Support custom CSV uploads and report downloads
- Prepare a college-level academic project with documentation and sample data

## 5. Scope of the Project
The dashboard is designed for academic analysis and is not intended to replace institutional ERP systems. It focuses on the analysis of student performance and attendance records, with filters for class, subject, semester, and grade. The application is built for demonstration and learning and supports both sample data and user-uploaded data.

## 6. Technologies Used
- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- CSV file handling
- ReportLab (for PDF report generation)

## 7. Dataset Description
The generated dataset is stored in `student_performance.csv`. It contains student-level academic records across several subjects and semesters. The dataset contains the following fields:
- Student_ID
- Student_Name
- Class
- Subject
- Semester
- Marks_Obtained
- Total_Marks
- Attendance_Percentage
- Grade
- Result

The actual generated dataset used in this project contains 1,863 student-subject records for 150 unique students, spread across four classes and six subjects.

## 8. System Architecture
The system architecture is simple and beginner-friendly:
1. Data generation script creates a realistic academic dataset
2. Streamlit app loads the dataset and performs validation
3. Filters and thresholds are applied dynamically
4. Charts and KPI metrics are computed from the active dataset
5. User can upload another CSV for analysis
6. Reports can be downloaded as CSV files within the same session

## 9. Data Cleaning and Preprocessing
The project performs several checks before analysis:
- Validate required columns
- Check for missing or blank values
- Ensure total marks are greater than zero
- Ensure marks obtained remain within range
- Ensure attendance remains between 0 and 100
- Identify duplicate subject-semester records
- Recalculate derived metrics such as percentage, grade, and result

## 10. Exploratory Data Analysis
The exploratory analysis includes subject-wise averages, class performance, grade spread, pass/fail distribution, semester trends, and attendance distribution. This helps identify stronger and weaker classes and subjects. It also allows the user to compare performance across classes and understand how marks and attendance behave together.

## 11. Data Analysis Methodology
The analysis calculates:
- Marks percentage = (Marks_Obtained / Total_Marks) * 100
- Average marks = arithmetic mean of marks percentages
- Average attendance = arithmetic mean of attendance percentages
- Pass rate = (number of pass records / total records) * 100

Filters are applied by class, subject, semester, and grade. These filters affect all KPI cards, charts, tables, and downloadable reports.

## 12. KPI Calculations
The dashboard uses the following KPIs:
- Total Students: unique student count in the filtered dataset
- Average Marks: mean marks percentage
- Average Attendance: mean attendance percentage
- Pass Rate: percentage of passing records
- Failing Records: count of records below the pass threshold
- At-Risk Students: unique students flagged on the basis of low marks and/or low attendance

The sample dataset produced the following observed summary:
- Total records: 1,863
- Unique students: 150
- Average marks: 67.77%
- Average attendance: 75.05%
- Pass rate: 92.11%
- Failing records: 147

These values were calculated directly from the generated file `student_performance.csv` and may change when filters or uploaded data are applied.

## 13. Dashboard Design
The dashboard uses a clean light theme with a blue-and-white academic style. A sidebar contains filters and dashboard controls. Metric cards appear across the top for key indicators. The visual layout is organized into sections for overview, academic analysis, attendance analysis, risk analysis, and student records. Plotly charts are interactive and support hover information.

## 14. Explanation of Visualizations
The dashboard includes the following visualizations:
- Subject-wise average marks bar chart
- Class-wise academic performance bar chart
- Grade distribution chart
- Pass vs. fail analysis
- Semester-wise performance line chart
- Subject comparison across classes
- Attendance by class bar chart
- Attendance histogram
- Attendance vs. academic performance scatter plot
- Risk category distribution chart

These charts help identify patterns in classroom outcomes, subject strengths, and students needing intervention.

## 15. Student Risk Identification Methodology
Student risk is evaluated on a student-level basis rather than by counting each subject record separately. This prevents the same student from being counted multiple times in a single risk summary. The system groups student records by `Student_ID`, `Student_Name`, and `Class`, then calculates average marks and average attendance. A student is flagged as high risk or medium risk when academic performance and/or attendance fall below set thresholds. This makes the risk model transparent and easy to explain.

## 16. Implementation Details
The main streaming logic is implemented in `app.py`. It contains functions for:
- Data loading
- Validation
- Calculation of marks percentage and grades
- Risk summary generation
- Filtering logic
- Chart rendering
- CSV export

The data generator is implemented in `generate_dataset.py` and produces a realistic sample file. The project is intentionally structured to be understandable for beginners while still being practically useful.

## 17. Testing and Validation
The implementation was validated for:
- Successful dataset generation
- Correct file loading
- Valid grade calculation
- Valid pass/fail classification
- Data validation for missing columns and invalid values
- Correct filter application
- Dashboard startup using Streamlit
- CSV upload processing and error handling

The sample dataset generation was tested successfully and the app was started in headless mode using Streamlit.

## 18. Key Findings from the Sample Dataset
The generated sample dataset shows that:
- Average marks are around 67.77%
- Average attendance is around 75.05%
- Pass rate is approximately 92.11%
- BCA 1B has the highest average marks among the four classes in the sample data
- Operating Systems and Mathematics are among the strongest average-performing subjects
- A number of students fall below the default risk threshold and would benefit from mentoring or follow-up

These are observed results from the generated dataset and may change as the user filters or uploads new data.

## 19. Limitations
- The sample dataset is synthetic and does not represent a real institutional database
- The dashboard is designed for demonstration and educational use
- Custom datasets should be cleaned before upload to avoid validation errors
- Risk rules are simplified and can be adjusted by the user depending on institution policy

## 20. Future Enhancements
- Add login and role-based access for teachers and administrators
- Add database storage for uploaded records
- Add more advanced predictive analytics
- Export PDF reports and dashboards directly
- Add student-wise drill-down pages
- Include academic trend forecasting by semester and subject

## 21. Conclusion
This project demonstrates how Python, Streamlit, and data analysis libraries can be combined to build an effective academic dashboard. It equips teachers and administrators with a practical way to analyze attendance, performance, and risk while using realistic sample data. The application is simple, interactive, and ready for academic submission.

## 22. Instructions to Run the Application
```bash
pip install -r requirements.txt
streamlit run app.py
```

If the sample dataset needs to be regenerated:
```bash
python generate_dataset.py
```

## 23. References
This project uses common data analysis workflows and standard Python visualization libraries. Additional enhancements can be added based on institutional requirements.
