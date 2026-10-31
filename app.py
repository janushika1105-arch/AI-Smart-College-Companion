
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from agents.attendance_agent import AttendanceAgent
from agents.performance_agent import PerformanceAgent
from agents.skill_agent import SkillAgent
from agents.job_agent import JobAgent
from agents.placement_agent import PlacementAgent
from agents.course_agent import CourseAgent
from agents.event_agent import EventAgent
from agents.resume_agent import ResumeAgent


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Smart College Companion",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Smart College Companion")
st.write("Collaborative Multi-Agent System")

st.markdown("---")


# --------------------------------
# CREATE AGENT OBJECTS
# --------------------------------

attendance_agent = AttendanceAgent()
performance_agent = PerformanceAgent()
skill_agent = SkillAgent()
job_agent = JobAgent()
placement_agent = PlacementAgent()
course_agent = CourseAgent()
event_agent = EventAgent()
resume_agent = ResumeAgent()


# --------------------------------
# EXCEL AND CSV UPLOAD
# --------------------------------

st.header("📂 Upload Student Database")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

data = None

if uploaded_file is not None:

    if uploaded_file.name.lower().endswith(".csv"):

        data = pd.read_csv(uploaded_file)

    else:

        excel_file = pd.ExcelFile(uploaded_file)

        sheet_name = st.selectbox(
            "Select Excel Worksheet",
            excel_file.sheet_names
        )

        data = pd.read_excel(
            excel_file,
            sheet_name=sheet_name
        )

    st.success("Student database uploaded successfully!")

else:

    try:
        data = pd.read_csv("students.csv")
        st.info("Using default student database.")

    except FileNotFoundError:
        st.warning("Please upload a student database.")
        st.stop()


# --------------------------------
# DATA VALIDATION
# --------------------------------

data.columns = data.columns.astype(str).str.strip()

required_columns = [
    "Name",
    "Attendance",
    "Maths",
    "Python",
    "AI",
    "SQL",
    "Excel",
    "PowerBI",
    "CGPA",
    "Communication"
]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:

    st.error(
        f"Missing required columns: {missing_columns}"
    )

    st.write("Available columns:", list(data.columns))
    st.stop()

if data.empty:
    st.error("The uploaded dataset is empty.")
    st.stop()

data = data.dropna(subset=["Name"]).copy()

if data.empty:
    st.error("No valid student records found.")
    st.stop()


numeric_columns = [
    "Attendance",
    "Maths",
    "Python",
    "AI",
    "SQL",
    "Excel",
    "PowerBI",
    "CGPA"
]

for col in numeric_columns:
    data[col] = pd.to_numeric(
        data[col], errors="coerce"
    )

data = data.dropna(subset=numeric_columns)

if data.empty:
    st.error("No valid numeric student records found.")
    st.stop()


# --------------------------------
# DATASET INFORMATION
# --------------------------------

st.subheader("📊 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(data))
col2.metric("Total Columns", len(data.columns))
col3.metric("Average Attendance",
            f"{data['Attendance'].mean():.1f}%")

with st.expander("Preview Student Database"):
    st.dataframe(data, use_container_width=True)


# --------------------------------
# ANALYZE ALL STUDENTS
# --------------------------------

analytics = []

for _, row in data.iterrows():

    attendance = attendance_agent.check_attendance(
        row["Attendance"]
    )

    performance = performance_agent.check_performance(
        row["Maths"],
        row["Python"],
        row["AI"]
    )

    strong_skills, missing_skills = (
        skill_agent.analyze_skills(
            row["Python"],
            row["SQL"],
            row["Excel"],
            row["PowerBI"]
        )
    )

    job = job_agent.recommend_job(strong_skills)

    placement = placement_agent.check_placement(
        row["Attendance"],
        row["CGPA"],
        row["Communication"]
    )

    resume_score, improvements = (
        resume_agent.calculate_score(
            row["Attendance"],
            row["CGPA"],
            row["Communication"],
            strong_skills,
            placement,
            missing_skills
        )
    )

    analytics.append({
        "Name": row["Name"],
        "Attendance": row["Attendance"],
        "CGPA": row["CGPA"],
        "Maths": row["Maths"],
        "Python": row["Python"],
        "AI": row["AI"],
        "SQL": row["SQL"],
        "Excel": row["Excel"],
        "PowerBI": row["PowerBI"],
        "Communication": row["Communication"],
        "Attendance Status": attendance,
        "Performance Status": performance,
        "Strong Skills": ", ".join(map(str, strong_skills)),
        "Missing Skills": ", ".join(map(str, missing_skills)),
        "Recommended Job": job,
        "Placement Status": placement,
        "Resume Score": resume_score,
        "Resume Improvements": ", ".join(map(str, improvements))
    })

analytics_df = pd.DataFrame(analytics)


# --------------------------------
# MAIN ANALYTICS DASHBOARD
# --------------------------------

st.markdown("---")
st.header("📈 Student Analytics Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", len(data))

c2.metric(
    "Average Attendance",
    f"{data['Attendance'].mean():.1f}%"
)

c3.metric(
    "Average CGPA",
    f"{data['CGPA'].mean():.2f}"
)

c4.metric(
    "Average Resume Score",
    f"{analytics_df['Resume Score'].mean():.1f}/100"
)


# --------------------------------
# ATTENDANCE ANALYSIS
# --------------------------------

st.markdown("---")
st.header("📅 Attendance Analysis")

attendance_fig = px.bar(
    data,
    x="Name",
    y="Attendance",
    color="Attendance",
    text="Attendance",
    title="Student Attendance Percentage",
    color_continuous_scale="Blues"
)

attendance_fig.add_hline(
    y=75,
    line_dash="dash",
    annotation_text="75% Attendance Threshold"
)

attendance_fig.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(
    attendance_fig,
    use_container_width=True
)


# --------------------------------
# PERFORMANCE ANALYSIS
# --------------------------------

st.markdown("---")
st.header("📚 Academic Performance Analysis")

performance_data = data[
    ["Name", "Maths", "Python", "AI"]
].melt(
    id_vars="Name",
    var_name="Subject",
    value_name="Marks"
)

performance_fig = px.bar(
    performance_data,
    x="Name",
    y="Marks",
    color="Subject",
    barmode="group",
    title="Subject-wise Student Performance"
)

st.plotly_chart(
    performance_fig,
    use_container_width=True
)


# --------------------------------
# SKILL ANALYSIS
# --------------------------------

st.markdown("---")
st.header("💻 Technical Skills Analysis")

skill_data = data[
    ["Python", "SQL", "Excel", "PowerBI"]
].mean().reset_index()

skill_data.columns = ["Skill", "Average Score"]

skill_fig = px.bar(
    skill_data,
    x="Skill",
    y="Average Score",
    color="Skill",
    title="Average Technical Skills Performance",
    text_auto=".1f"
)

st.plotly_chart(
    skill_fig,
    use_container_width=True
)


# --------------------------------
# PLACEMENT ANALYSIS
# --------------------------------

st.markdown("---")
st.header("🎯 Placement Eligibility Analysis")

placement_counts = analytics_df[
    "Placement Status"
].value_counts().reset_index()

placement_counts.columns = [
    "Placement Status",
    "Students"
]

placement_fig = px.pie(
    placement_counts,
    names="Placement Status",
    values="Students",
    title="Student Placement Eligibility",
    hole=0.4
)

st.plotly_chart(
    placement_fig,
    use_container_width=True
)


# --------------------------------
# RESUME SCORE ANALYSIS
# --------------------------------

st.markdown("---")
st.header("📄 Resume Score Analysis")

resume_fig = px.bar(
    analytics_df,
    x="Name",
    y="Resume Score",
    color="Resume Score",
    text="Resume Score",
    title="Student Resume Scores",
    color_continuous_scale="Viridis"
)

resume_fig.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(
    resume_fig,
    use_container_width=True
)


# --------------------------------
# INDIVIDUAL STUDENT REPORT
# --------------------------------

st.markdown("---")
st.header("👨‍🎓 Individual Student Report")

student = st.selectbox(
    "Select Student",
    data["Name"].tolist()
)

row = data[data["Name"] == student].iloc[0]

result = analytics_df[
    analytics_df["Name"] == student
].iloc[0]


col1, col2 = st.columns(2)

with col1:

    st.success(
        f"Attendance: {result['Attendance Status']}"
    )

    st.info(
        f"Performance: {result['Performance Status']}"
    )

    st.write(
        f"Recommended Job: {result['Recommended Job']}"
    )

with col2:

    st.success(
        f"Placement: {result['Placement Status']}"
    )

    st.metric(
        "Resume Score",
        f"{result['Resume Score']}/100"
    )


st.subheader("Strong Skills")
st.write(result["Strong Skills"])

st.subheader("Missing Skills")
st.write(result["Missing Skills"])

st.subheader("Resume Improvements")
st.write(result["Resume Improvements"])


# --------------------------------
# COURSE RECOMMENDATIONS
# --------------------------------

courses = course_agent.recommend_courses(
    skill_agent.analyze_skills(
        row["Python"],
        row["SQL"],
        row["Excel"],
        row["PowerBI"]
    )[1]
)

st.subheader("🎓 Recommended Courses")

if courses:
    for course in courses:
        st.write("•", course)
else:
    st.success("No Courses Required")


# --------------------------------
# EVENT RECOMMENDATIONS
# --------------------------------

events = event_agent.recommend_events(
    skill_agent.analyze_skills(
        row["Python"],
        row["SQL"],
        row["Excel"],
        row["PowerBI"]
    )[0],
    result["Placement Status"]
)

st.subheader("🎉 Recommended Events")

if events:
    for event in events:
        st.write("•", event)
else:
    st.info("No Events Available")


# --------------------------------
# POWER BI DATA EXPORT
# --------------------------------

st.markdown("---")
st.header("📊 Microsoft Power BI Integration")

st.write(
    "Download the processed student analytics dataset "
    "and import it into Microsoft Power BI Desktop."
)

st.subheader("Power BI Dataset Preview")

st.dataframe(
    analytics_df,
    use_container_width=True
)

# CSV Export

csv_data = analytics_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Power BI CSV Dataset",
    data=csv_data,
    file_name="Smart_College_Analytics.csv",
    mime="text/csv"
)

# Excel Export

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    analytics_df.to_excel(
        writer,
        sheet_name="Student Analytics",
        index=False
    )

    data.to_excel(
        writer,
        sheet_name="Original Student Data",
        index=False
    )

st.download_button(
    label="⬇️ Download Power BI Excel Dataset",
    data=excel_buffer.getvalue(),
    file_name="Smart_College_Analytics.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# --------------------------------
# FOOTER
# --------------------------------

st.markdown("---")

st.caption(
    "AI Smart College Companion | "
    "Collaborative Multi-Agent System"
)
