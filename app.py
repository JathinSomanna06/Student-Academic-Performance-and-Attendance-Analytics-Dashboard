from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from generate_dataset import generate_dataset

DATASET_PATH = Path(__file__).resolve().parent / "student_performance.csv"
PASSING_THRESHOLD_DEFAULT = 40.0
ATTENDANCE_THRESHOLD_DEFAULT = 75.0
RISK_THRESHOLD_DEFAULT = 60.0
REQUIRED_COLUMNS = [
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


@st.cache_data
def load_base_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def ensure_sample_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        generated = generate_dataset()
        generated.to_csv(DATASET_PATH, index=False)
    return load_base_data(DATASET_PATH)


def calculate_grade(marks_percentage: float) -> str:
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


def add_derived_columns(df: pd.DataFrame, pass_threshold: float = PASSING_THRESHOLD_DEFAULT) -> pd.DataFrame:
    if df is None or df.empty:
        return df.copy()

    result = df.copy()
    result["Marks_Obtained"] = pd.to_numeric(result["Marks_Obtained"], errors="coerce")
    result["Total_Marks"] = pd.to_numeric(result["Total_Marks"], errors="coerce")
    result["Attendance_Percentage"] = pd.to_numeric(result["Attendance_Percentage"], errors="coerce")
    result["Semester"] = pd.to_numeric(result["Semester"], errors="coerce")
    result["Marks_Percentage"] = np.where(
        result["Total_Marks"].gt(0),
        (result["Marks_Obtained"] / result["Total_Marks"]) * 100,
        0.0,
    )
    result["Grade"] = result["Marks_Percentage"].map(calculate_grade)
    result["Result"] = np.where(result["Marks_Percentage"] >= pass_threshold, "Pass", "Fail")
    return result


def validate_uploaded_csv(df: pd.DataFrame):
    if df is None:
        return None, ["Uploaded file could not be read."]
    if df.empty:
        return None, ["Uploaded CSV is empty."]

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        return None, [f"Missing required columns: {', '.join(missing)}"]

    errors = []
    cleaned = df.copy().replace({"": pd.NA, None: pd.NA})

    for column in ["Student_ID", "Student_Name", "Class", "Subject"]:
        if cleaned[column].isna().any() or (cleaned[column].astype(str).str.strip() == "").any():
            errors.append(f"{column} contains missing or blank values.")

    numeric_columns = ["Marks_Obtained", "Total_Marks", "Attendance_Percentage", "Semester"]
    try:
        for column in numeric_columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="raise")
    except Exception:
        errors.append("Numeric columns contain invalid values.")

    if (cleaned["Total_Marks"] <= 0).any():
        errors.append("Total_Marks must be greater than zero in every row.")
    if ((cleaned["Marks_Obtained"] < 0) | (cleaned["Marks_Obtained"] > cleaned["Total_Marks"])).any():
        errors.append("Marks_Obtained must stay between 0 and Total_Marks.")
    if ((cleaned["Attendance_Percentage"] < 0) | (cleaned["Attendance_Percentage"] > 100)).any():
        errors.append("Attendance_Percentage must be between 0 and 100.")
    if cleaned.duplicated(subset=["Student_ID", "Student_Name", "Class", "Subject", "Semester"]).any():
        errors.append("Duplicate student-subject-semester records were found.")

    if errors:
        return None, errors

    cleaned = cleaned.sort_values(["Student_ID", "Semester", "Subject"]).reset_index(drop=True)
    cleaned = add_derived_columns(cleaned)
    return cleaned, []


@st.cache_data
def build_student_risk_summary(df: pd.DataFrame, attendance_threshold: float, risk_threshold: float) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["Student_ID", "Student_Name", "Class", "Avg_Marks", "Avg_Attendance", "Failing_Records", "Low_Attendance_Records", "Risk_Category", "Support_Action"])

    student_summary = (
        df.groupby(["Student_ID", "Student_Name", "Class"], as_index=False)
        .agg(
            Avg_Marks=("Marks_Percentage", "mean"),
            Avg_Attendance=("Attendance_Percentage", "mean"),
            Failing_Records=("Result", lambda s: int((s == "Fail").sum())),
            Low_Attendance_Records=("Attendance_Percentage", lambda s: int((s < attendance_threshold).sum())),
        )
        .copy()
    )

    conditions = [
        (student_summary["Avg_Marks"] < risk_threshold) & (student_summary["Avg_Attendance"] < attendance_threshold),
        (student_summary["Avg_Marks"] < risk_threshold) | (student_summary["Avg_Attendance"] < attendance_threshold),
    ]
    choices = ["High Risk", "Medium Risk"]
    student_summary["Risk_Category"] = np.select(conditions, choices, default="Low Risk")

    action_map = {
        "High Risk": "Immediate academic review, attendance follow-up, and individual mentoring.",
        "Medium Risk": "Academic mentoring and attendance monitoring.",
        "Low Risk": "Continue regular academic monitoring.",
    }
    student_summary["Support_Action"] = student_summary["Risk_Category"].map(action_map)
    return student_summary


def apply_filters(df: pd.DataFrame, selected: dict) -> pd.DataFrame:
    filtered = df.copy()
    for column, values in selected.items():
        if column == "Class" and values:
            filtered = filtered[filtered["Class"].isin(values)]
        elif column == "Subject" and values:
            filtered = filtered[filtered["Subject"].isin(values)]
        elif column == "Semester" and values:
            filtered = filtered[filtered["Semester"].astype(str).isin([str(v) for v in values])]
        elif column == "Grade" and values:
            filtered = filtered[filtered["Grade"].isin(values)]
        elif values == []:
            return filtered.iloc[0:0].copy()
    return filtered.reset_index(drop=True)


def get_filter_defaults(df: pd.DataFrame):
    class_values = sorted(df["Class"].dropna().unique().tolist())
    subject_values = sorted(df["Subject"].dropna().unique().tolist())
    semester_values = sorted(pd.to_numeric(df["Semester"], errors="coerce").dropna().unique().astype(int).tolist())
    grade_values = sorted(df["Grade"].dropna().unique().tolist())
    return {
        "Class": class_values,
        "Subject": subject_values,
        "Semester": semester_values,
        "Grade": grade_values,
    }


def render_kpi_cards(df: pd.DataFrame, risk_summary: pd.DataFrame, pass_threshold: float):
    if df.empty:
        st.info("No KPI data available for the current filters.")
        return

    total_students = df["Student_ID"].nunique()
    average_marks = df["Marks_Percentage"].mean()
    average_attendance = df["Attendance_Percentage"].mean()
    pass_count = (df["Result"] == "Pass").sum()
    fail_count = (df["Result"] == "Fail").sum()
    pass_rate = (pass_count / len(df)) * 100 if len(df) else 0
    at_risk_students = risk_summary[risk_summary["Risk_Category"].isin(["High Risk", "Medium Risk"])].shape[0]

    cards = [
        ("Total Students", total_students, "Unique students"),
        ("Average Marks", f"{average_marks:.2f}%", "Across selected records"),
        ("Average Attendance", f"{average_attendance:.2f}%", "Across selected records"),
        ("Pass Rate", f"{pass_rate:.2f}%", f"Threshold: {pass_threshold}%"),
        ("Failing Records", fail_count, "Below threshold"),
        ("At-Risk Students", at_risk_students, "Risk category summary"),
    ]

    columns = st.columns(6)
    for column, (label, value, delta) in zip(columns, cards):
        column.metric(label=label, value=value, delta=delta)


def render_subject_marks_chart(df: pd.DataFrame):
    if df.empty:
        return
    fig = px.bar(
        df.groupby("Subject", as_index=False)["Marks_Percentage"].mean().sort_values("Marks_Percentage", ascending=False),
        x="Subject",
        y="Marks_Percentage",
        title="Subject-wise Average Marks",
        labels={"Subject": "Subject", "Marks_Percentage": "Average Marks (%)"},
        color="Marks_Percentage",
        text_auto=".2f",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_class_performance_chart(df: pd.DataFrame):
    if df.empty:
        return
    fig = px.bar(
        df.groupby("Class", as_index=False)["Marks_Percentage"].mean().sort_values("Marks_Percentage", ascending=False),
        x="Class",
        y="Marks_Percentage",
        title="Class-wise Academic Performance",
        labels={"Class": "Class", "Marks_Percentage": "Average Marks (%)"},
        color="Marks_Percentage",
        text_auto=".2f",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_grade_distribution_chart(df: pd.DataFrame):
    if df.empty:
        return
    counts = df["Grade"].value_counts().reindex(["A", "B", "C", "D", "E", "F"], fill_value=0)
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title="Grade Distribution",
        labels={"x": "Grade", "y": "Number of Records"},
        color=counts.values,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_pass_fail_chart(df: pd.DataFrame):
    if df.empty:
        return
    counts = df["Result"].value_counts().reindex(["Pass", "Fail"], fill_value=0)
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title="Pass vs. Fail Analysis",
        labels={"x": "Result", "y": "Number of Records"},
        color=counts.index,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_semester_line_chart(df: pd.DataFrame):
    if df.empty:
        return
    fig = px.line(
        df.groupby("Semester", as_index=False)["Marks_Percentage"].mean().sort_values("Semester"),
        x="Semester",
        y="Marks_Percentage",
        markers=True,
        title="Semester-wise Performance",
        labels={"Semester": "Semester", "Marks_Percentage": "Average Marks (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_subject_comparison_chart(df: pd.DataFrame):
    if df.empty:
        return
    data = df.groupby(["Class", "Subject"], as_index=False)["Marks_Percentage"].mean()
    fig = px.line(
        data,
        x="Class",
        y="Marks_Percentage",
        color="Subject",
        markers=True,
        title="Subject Comparison Across Classes",
        labels={"Class": "Class", "Marks_Percentage": "Average Marks (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_attendance_by_class_chart(df: pd.DataFrame):
    if df.empty:
        return
    fig = px.bar(
        df.groupby("Class", as_index=False)["Attendance_Percentage"].mean().sort_values("Attendance_Percentage", ascending=False),
        x="Class",
        y="Attendance_Percentage",
        title="Average Attendance by Class",
        labels={"Class": "Class", "Attendance_Percentage": "Average Attendance (%)"},
        color="Attendance_Percentage",
        text_auto=".2f",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_attendance_histogram(df: pd.DataFrame):
    if df.empty:
        return
    fig = px.histogram(
        df,
        x="Attendance_Percentage",
        nbins=25,
        title="Attendance Distribution",
        labels={"Attendance_Percentage": "Attendance (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_attendance_vs_marks_chart(df: pd.DataFrame):
    if df.empty:
        return
    fig = px.scatter(
        df,
        x="Attendance_Percentage",
        y="Marks_Percentage",
        hover_data={"Student_Name": True, "Class": True, "Subject": True, "Semester": True},
        title="Attendance vs. Academic Performance",
        labels={"Attendance_Percentage": "Attendance (%)", "Marks_Percentage": "Marks (%)"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_low_attendance_table(df: pd.DataFrame, attendance_threshold: float):
    if df.empty:
        return
    table = df[df["Attendance_Percentage"] < attendance_threshold][[
        "Student_ID",
        "Student_Name",
        "Class",
        "Subject",
        "Semester",
        "Attendance_Percentage",
        "Marks_Percentage",
    ]].copy()
    if table.empty:
        st.info(f"No records fall below the current attendance threshold of {attendance_threshold}%.")
        return
    st.dataframe(table.sort_values(["Attendance_Percentage", "Marks_Percentage"], ascending=[True, False]), use_container_width=True, hide_index=True)


def render_risk_summary(df: pd.DataFrame, attendance_threshold: float, risk_threshold: float):
    if df.empty:
        return
    summary = build_student_risk_summary(df, attendance_threshold, risk_threshold)
    if summary.empty:
        return
    cols = ["Student_ID", "Student_Name", "Class", "Avg_Marks", "Avg_Attendance", "Failing_Records", "Low_Attendance_Records", "Risk_Category", "Support_Action"]
    st.dataframe(summary[cols].sort_values(["Risk_Category", "Avg_Marks"], ascending=[False, True]), use_container_width=True, hide_index=True)

    risk_counts = summary["Risk_Category"].value_counts().reindex(["High Risk", "Medium Risk", "Low Risk"], fill_value=0)
    fig = px.bar(
        x=risk_counts.index,
        y=risk_counts.values,
        title="Risk Category Distribution",
        labels={"x": "Risk Category", "y": "Students"},
        color=risk_counts.index,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_student_records_table(df: pd.DataFrame):
    if df.empty:
        st.warning("No student records match the selected filters.")
        return
    table = df[[
        "Student_ID",
        "Student_Name",
        "Class",
        "Subject",
        "Semester",
        "Marks_Obtained",
        "Total_Marks",
        "Marks_Percentage",
        "Attendance_Percentage",
        "Grade",
        "Result",
    ]].copy()
    table["Marks_Percentage"] = table["Marks_Percentage"].round(2)
    table["Attendance_Percentage"] = table["Attendance_Percentage"].round(2)
    st.caption(f"Showing {len(table)} records")
    st.dataframe(table, use_container_width=True, hide_index=True)


def render_report_downloads(df: pd.DataFrame, risk_summary: pd.DataFrame, attendance_threshold: float):
    if df.empty:
        st.info("Reports are not available because the current dataset is empty.")
        return

    filtered_csv = df.to_csv(index=False)
    at_risk_csv = risk_summary.to_csv(index=False)
    subject_report = (
        df.groupby("Subject", as_index=False).agg(Average_Marks_Percentage=("Marks_Percentage", "mean"), Records=("Subject", "count"))
        .sort_values("Average_Marks_Percentage", ascending=False)
    )
    class_report = (
        df.groupby("Class", as_index=False).agg(Average_Marks_Percentage=("Marks_Percentage", "mean"), Records=("Class", "count"))
        .sort_values("Average_Marks_Percentage", ascending=False)
    )
    semester_report = (
        df.groupby("Semester", as_index=False).agg(Average_Marks_Percentage=("Marks_Percentage", "mean"), Records=("Semester", "count"))
        .sort_values("Semester")
    )
    low_attendance = df[df["Attendance_Percentage"] < attendance_threshold]

    reports = [
        ("Filtered Student Records", filtered_csv, "filtered_student_records.csv"),
        ("At-Risk Student Report", at_risk_csv, "at_risk_student_report.csv"),
        ("Low Attendance Report", low_attendance.to_csv(index=False), "low_attendance_report.csv"),
        ("Subject Performance Report", subject_report.to_csv(index=False), "subject_performance_report.csv"),
        ("Class Performance Report", class_report.to_csv(index=False), "class_performance_report.csv"),
        ("Semester Performance Report", semester_report.to_csv(index=False), "semester_performance_report.csv"),
    ]

    cols = st.columns(3)
    for index, (label, csv_data, filename) in enumerate(reports):
        column = cols[index % 3]
        column.download_button(label, data=csv_data, file_name=filename, mime="text/csv", use_container_width=True)


def render_about_info():
    st.markdown(
        """
        ### Analysis Rules
        - Marks percentage = (Marks_Obtained / Total_Marks) * 100
        - Average marks and attendance are calculated from the active filter selection.
        - Default pass threshold: 40%
        - Grade scale: A >= 90, B 80-89.99, C 70-79.99, D 60-69.99, E 40-59.99, F < 40
        - Risk evaluation aggregates by student to avoid double-counting the same student across multiple subject records.
        """
    )


def main():
    st.set_page_config(page_title="Student Academic Dashboard", page_icon="??", layout="wide")
    st.title("Student Academic Performance and Attendance Analytics Dashboard")
    st.caption("Interactive academic dashboard for exploring attendance, performance, and student risk.")

    sample_df = ensure_sample_dataset()
    if "current_dataset" not in st.session_state:
        st.session_state.current_dataset = sample_df.copy()
        st.session_state.data_source = "sample"

    sidebar = st.sidebar
    sidebar.title("Dashboard Controls")
    pass_threshold = sidebar.slider("Passing threshold (%)", min_value=30.0, max_value=70.0, value=PASSING_THRESHOLD_DEFAULT, step=1.0)
    attendance_threshold = sidebar.slider("Attendance threshold (%)", min_value=40.0, max_value=95.0, value=ATTENDANCE_THRESHOLD_DEFAULT, step=1.0)
    risk_threshold = sidebar.slider("Risk threshold (%)", min_value=40.0, max_value=90.0, value=RISK_THRESHOLD_DEFAULT, step=1.0)

    uploaded_file = sidebar.file_uploader("Upload CSV data", type=["csv"])
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            validated_df, errors = validate_uploaded_csv(raw_df)
            if errors:
                sidebar.error("Uploaded dataset is invalid.")
                for err in errors:
                    sidebar.write(f"- {err}")
            else:
                st.session_state.current_dataset = validated_df
                st.session_state.data_source = "uploaded"
                st.sidebar.success("Uploaded dataset validated and loaded.")
        except Exception as exc:
            sidebar.error(f"Unable to read uploaded file: {exc}")

    if sidebar.button("Use sample dataset"):
        st.session_state.current_dataset = sample_df.copy()
        st.session_state.data_source = "sample"

    current_df = st.session_state.current_dataset.copy()
    current_df = add_derived_columns(current_df, pass_threshold)

    defaults = get_filter_defaults(current_df)
    selected = {
        "Class": sidebar.multiselect("Class", options=defaults["Class"], default=defaults["Class"], key="class_filter"),
        "Subject": sidebar.multiselect("Subject", options=defaults["Subject"], default=defaults["Subject"], key="subject_filter"),
        "Semester": sidebar.multiselect("Semester", options=defaults["Semester"], default=defaults["Semester"], key="semester_filter"),
        "Grade": sidebar.multiselect("Grade", options=defaults["Grade"], default=defaults["Grade"], key="grade_filter"),
    }

    filtered_df = apply_filters(current_df, selected)
    risk_summary = build_student_risk_summary(filtered_df, attendance_threshold, risk_threshold)

    if filtered_df.empty:
        st.warning("The active filters remove all records. Please adjust the filters or upload another dataset.")
        st.stop()

    render_kpi_cards(filtered_df, risk_summary, pass_threshold)

    st.subheader("Overview Dashboard")
    cols = st.columns(2)
    with cols[0]:
        render_subject_marks_chart(filtered_df)
    with cols[1]:
        render_class_performance_chart(filtered_df)

    st.subheader("Academic Performance Analysis")
    a, b = st.columns(2)
    with a:
        render_grade_distribution_chart(filtered_df)
    with b:
        render_pass_fail_chart(filtered_df)
    c, d = st.columns(2)
    with c:
        render_semester_line_chart(filtered_df)
    with d:
        render_subject_comparison_chart(filtered_df)

    st.subheader("Attendance Analysis")
    e, f = st.columns(2)
    with e:
        render_attendance_by_class_chart(filtered_df)
    with f:
        render_attendance_histogram(filtered_df)
    render_attendance_vs_marks_chart(filtered_df)

    st.subheader("Low Attendance Report")
    render_low_attendance_table(filtered_df, attendance_threshold)

    st.subheader("Student Risk Analysis")
    render_risk_summary(filtered_df, attendance_threshold, risk_threshold)

    st.subheader("Student Records")
    render_student_records_table(filtered_df)

    st.subheader("Data Upload and Reports")
    st.caption(f"Current dataset source: {st.session_state.data_source.title()}")
    render_report_downloads(filtered_df, risk_summary, attendance_threshold)
    render_about_info()


if __name__ == "__main__":
    main()
