from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

OUTPUT_FILE = "project_report.pdf"


def build_pdf():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=16,
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=18,
        spaceAfter=8,
    )
    body_style = styles["BodyText"]

    content = [
        Paragraph("Student Academic Performance and Attendance Analytics Dashboard", title_style),
        Paragraph("Student Name: [Student Name]", body_style),
        Paragraph("Registration Number: [Registration Number]", body_style),
        Paragraph("College: [College Name]", body_style),
        Paragraph("Department: [Department Name]", body_style),
        Paragraph("Submission Date: [DD/MM/YYYY]", body_style),
        Spacer(1, 12),
        Paragraph("Abstract", heading_style),
        Paragraph(
            "This project presents a professional and interactive dashboard implemented in Python and Streamlit for the analysis of student academic performance and attendance. The application helps teachers and administrators monitor subject performance, compare classes, identify at-risk students, and evaluate attendance trends. It loads a realistic generated dataset, supports filtering, and allows CSV upload for custom analysis.",
            body_style,
        ),
        Paragraph("Key generated dataset findings", heading_style),
        Paragraph("- Total records: 1863", body_style),
        Paragraph("- Unique students: 150", body_style),
        Paragraph("- Average marks: 67.77%", body_style),
        Paragraph("- Average attendance: 75.05%", body_style),
        Paragraph("- Pass rate: 92.11%", body_style),
        Paragraph("- Failing records: 147", body_style),
        Paragraph("Project objectives", heading_style),
        ListFlowable(
            [
                ListItem(Paragraph("Build an interactive academic dashboard using Streamlit.", body_style)),
                ListItem(Paragraph("Analyze marks, attendance, and outcomes across classes and semesters.", body_style)),
                ListItem(Paragraph("Identify students who need academic support or attendance follow-up.", body_style)),
                ListItem(Paragraph("Allow CSV uploads and downloadable reports.", body_style)),
            ],
            bulletType="bullet",
            leftIndent=20,
        ),
        Paragraph("Technologies used", heading_style),
        ListFlowable(
            [
                ListItem(Paragraph("Python", body_style)),
                ListItem(Paragraph("Pandas", body_style)),
                ListItem(Paragraph("NumPy", body_style)),
                ListItem(Paragraph("Streamlit", body_style)),
                ListItem(Paragraph("Plotly", body_style)),
                ListItem(Paragraph("ReportLab", body_style)),
            ],
            bulletType="bullet",
            leftIndent=20,
        ),
        Paragraph("Implementation notes", heading_style),
        Paragraph(
            "The dashboard includes validation checks, feature filtering, risk analysis, student record tables, and CSV export functions. It is designed as a beginner-friendly academic tool and supports both the sample dataset and uploaded data.",
            body_style,
        ),
        Paragraph("Instructions to run", heading_style),
        ListFlowable(
            [
                ListItem(Paragraph("Install requirements with: pip install -r requirements.txt", body_style)),
                ListItem(Paragraph("Run the app with: streamlit run app.py", body_style)),
                ListItem(Paragraph("Regenerate the sample dataset with: python generate_dataset.py", body_style)),
            ],
            bulletType="bullet",
            leftIndent=20,
        ),
    ]

    document = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    document.build(content)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_pdf()
