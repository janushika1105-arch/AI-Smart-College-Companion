
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


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Smart College Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. PREMIUM DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #080d1c,
        #111b35,
        #17132e
    );
    color: #f1f5f9;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Headings */
h1 {
    color: #ffffff !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #c4b5fd !important;
    font-weight: 700 !important;
}

/* General text */
p, label, .stMarkdown {
    color: #e2e8f0;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #1e293b,
        #25204a
    );
    border: 1px solid #5145a8;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.25);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #a78bfa !important;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(
        90deg,
        #6366f1,
        #9333ea
    );
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(
        90deg,
        #8b5cf6,
        #c084fc
    );
    color: white;
    border: none;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #17223b;
    border: 1px dashed #8b5cf6;
    border-radius: 15px;
    padding: 15px;
}

/* Select boxes */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #202b45;
    border-color: #6255b5;
    border-radius: 10px;
    color: white;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #5145a8;
    border-radius: 12px;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #17223b;
    border: 1px solid #5145a8;
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101a33,
        #1b1740
    );
    border-right: 1px solid #5145a8;
}

/* Divider */
hr {
    border-color: #5145a8;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */
footer {
    visibility: hidden;
}

/* Sidebar text */
[data-testid="stSidebar"] p {
    color: #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. HERO SECTION
# ==========================================


# ==========================================
# 3. HERO SECTION
# ==========================================

st.markdown("""
<div style="background:linear-gradient(120deg,#312e81,#5b21b6,#1d4ed8);
padding:35px;border-radius:20px;margin-bottom:25px;
box-shadow:0 8px 30px rgba(0,0,0,0.3);">

<h1 style="color:white;margin:0;font-size:36px;">
🎓 AI Smart College Companion
</h1>

<p style="color:#e0e7ff;font-size:18px;margin-top:12px;">
Collaborative Multi-Agent System
</p>

<p style="color:#ddd6fe;font-size:14px;">
Smart Student Analytics |
AI Recommendations |
Placement Guidance
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR
# ==========================================

st.sidebar.markdown("""
<h2 style="color:#c4b5fd;">
🎓 Smart Companion
</h2>
<p style="color:#cbd5e1;">
Student Intelligence Dashboard
</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📌 Dashboard Features

- 📊 Student Analytics
- 📅 Attendance Analysis
- 📚 Academic Performance
- 💻 Technical Skills
- 🎯 Placement Eligibility
- 📄 Resume Score
- 🎓 Course Recommendations
- 🎉 Event Recommendations
- 📈 Power BI Export
""")

st.sidebar.markdown("---")

st.sidebar.info(
    "AI-powered student analysis "
    "using eight collaborative agents."
)


# ==========================================
# 5. CREATE AI AGENTS
# ==========================================

attendance_agent = AttendanceAgent()
performance_agent = PerformanceAgent()
skill_agent = SkillAgent()
job_agent = JobAgent()
placement_agent = PlacementAgent()
course_agent = CourseAgent()
event_agent = EventAgent()
resume_agent = ResumeAgent()


# ==========================================
# 6. CSV AND EXCEL UPLOAD
# ==========================================

st.header("📂 Upload Student Database")

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel Student Dataset",
    type=["csv", "xlsx"]
)

data = None

if uploaded_file is not None:

    try:

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

        st.success(
            "✅ Student Database Uploaded Successfully!"
        )

    except Exception as e:

        st.error(f"Unable to read the uploaded file: {e}")
        st.stop()

else:

    try:

        data = pd.read_csv("students.csv")

        st.info(
            "Using the default student database."
        )

    except FileNotFoundError:

        st.warning(
            "Please upload a CSV or Excel student database."
        )

        st.stop()


# ==========================================
# 7. DATA VALIDATION
# ==========================================

data.columns = (
    data.columns.astype(str).str.strip()
)

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

    st.write(
        "Available columns:",
        list(data.columns)
    )

    st.stop()


if data.empty:

    st.error("The uploaded dataset is empty.")
    st.stop()


data = data.dropna(
    subset=["Name"]
).copy()


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
        data[col],
        errors="coerce"
    )


data = data.dropna(
    subset=numeric_columns
).copy()


if data.empty:

    st.error(
        "No valid numeric student records found."
    )

    st.stop()


data = data.reset_index(drop=True)


# ==========================================
# 8. DATASET INFORMATION
# ==========================================

st.markdown("---")

st.header("📊 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Students",
    len(data)
)

col2.metric(
    "Total Columns",
    len(data.columns)
)

col3.metric(
    "Average Attendance",
    f"{data['Attendance'].mean():.1f}%"
)

with st.expander("👀 Preview Student Database"):

    st.dataframe(
        data,
        use_container_width=True
    )


# ==========================================
# 9. ANALYZE ALL STUDENTS
# ==========================================

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

    job = job_agent.recommend_job(
        strong_skills
    )

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

        "Strong Skills": ", ".join(
            map(str, strong_skills)
        ),

        "Missing Skills": ", ".join(
            map(str, missing_skills)
        ),

        "Recommended Job": job,

        "Placement Status": placement,

        "Resume Score": resume_score,

        "Resume Improvements": ", ".join(
            map(str, improvements)
        )

    })


analytics_df = pd.DataFrame(analytics)


# ==========================================
# 10. MAIN ANALYTICS DASHBOARD
# ==========================================

st.markdown("---")

st.header("📈 Student Analytics Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "👨‍🎓 Total Students",
    len(data)
)

c2.metric(
    "📅 Average Attendance",
    f"{data['Attendance'].mean():.1f}%"
)

c3.metric(
    "🎓 Average CGPA",
    f"{data['CGPA'].mean():.2f}"
)

c4.metric(
    "📄 Average Resume Score",
    f"{analytics_df['Resume Score'].mean():.1f}/100"
)


# ==========================================
# 11. ATTENDANCE ANALYSIS
# ==========================================

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
    line_color="#f87171",
    annotation_text="75% Attendance Threshold"
)

attendance_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    title_font=dict(
        size=20,
        color="#c4b5fd"
    ),
    yaxis_range=[0, 100],
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    attendance_fig,
    use_container_width=True
)


# ==========================================
# 12. PERFORMANCE ANALYSIS
# ==========================================

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
    title="Subject-wise Student Performance",
    color_discrete_sequence=[
        "#818cf8",
        "#a78bfa",
        "#38bdf8"
    ]
)

performance_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    title_font=dict(
        size=20,
        color="#c4b5fd"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    performance_fig,
    use_container_width=True
)


# ==========================================
# 13. TECHNICAL SKILLS ANALYSIS
# ==========================================

st.markdown("---")

st.header("💻 Technical Skills Analysis")

skill_data = data[
    ["Python", "SQL", "Excel", "PowerBI"]
].mean().reset_index()

skill_data.columns = [
    "Skill",
    "Average Score"
]

skill_fig = px.bar(
    skill_data,
    x="Skill",
    y="Average Score",
    color="Skill",
    title="Average Technical Skills Performance",
    text_auto=".1f",
    color_discrete_sequence=[
        "#818cf8",
        "#a78bfa",
        "#38bdf8",
        "#c084fc"
    ]
)

skill_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    title_font=dict(
        size=20,
        color="#c4b5fd"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    skill_fig,
    use_container_width=True
)


# ==========================================
# 14. PLACEMENT ANALYSIS
# ==========================================

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
    hole=0.5,
    color_discrete_sequence=[
        "#8b5cf6",
        "#38bdf8",
        "#f87171"
    ]
)

placement_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    title_font=dict(
        size=20,
        color="#c4b5fd"
    ),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    placement_fig,
    use_container_width=True
)


# ==========================================
# 15. RESUME SCORE ANALYSIS
# ==========================================

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
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    title_font=dict(
        size=20,
        color="#c4b5fd"
    ),
    yaxis_range=[0, 100],
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    resume_fig,
    use_container_width=True
)


# ==========================================
# 16. INDIVIDUAL STUDENT REPORT
# ==========================================

st.markdown("---")

st.header("👨‍🎓 Individual Student Report")

student = st.selectbox(
    "Select Student",
    data["Name"].tolist()
)

student_index = data.index[
    data["Name"] == student
][0]

row = data.loc[student_index]

result = analytics_df.loc[student_index]


col1, col2 = st.columns(2)

with col1:

    st.success(
        f"📅 Attendance: {result['Attendance Status']}"
    )

    st.info(
        f"📚 Performance: {result['Performance Status']}"
    )

    st.write(
        f"💼 Recommended Job: {result['Recommended Job']}"
    )

with col2:

    st.success(
        f"🎯 Placement: {result['Placement Status']}"
    )

    st.metric(
        "📄 Resume Score",
        f"{result['Resume Score']}/100"
    )


st.markdown("---")

st.subheader("💻 Strong Skills")

st.write(
    result["Strong Skills"]
    if result["Strong Skills"]
    else "No strong skills identified."
)

st.subheader("⚠️ Missing Skills")

st.write(
    result["Missing Skills"]
    if result["Missing Skills"]
    else "No missing skills identified."
)

st.subheader("🚀 Resume Improvements")

st.write(
    result["Resume Improvements"]
    if result["Resume Improvements"]
    else "No improvements suggested."
)


# ==========================================
# 17. COURSE RECOMMENDATIONS
# ==========================================

st.markdown("---")

st.header("🎓 Recommended Courses")

student_strong_skills, student_missing_skills = (
    skill_agent.analyze_skills(
        row["Python"],
        row["SQL"],
        row["Excel"],
        row["PowerBI"]
    )
)

courses = course_agent.recommend_courses(
    student_missing_skills
)

if courses:

    for course in courses:

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(120deg,#202b45,#312e5b);
                padding:15px;
                border-radius:12px;
                border-left:4px solid #a78bfa;
                margin-bottom:10px;
            ">
                🎓 {course}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success("✅ No Courses Required")


# ==========================================
# 18. EVENT RECOMMENDATIONS
# ==========================================

st.markdown("---")

st.header("🎉 Recommended Events")

events = event_agent.recommend_events(
    student_strong_skills,
    result["Placement Status"]
)

if events:

    for event in events:

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(120deg,#202b45,#312e5b);
                padding:15px;
                border-radius:12px;
                border-left:4px solid #38bdf8;
                margin-bottom:10px;
            ">
                🎉 {event}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info("No Events Available")


# ==========================================
# 19. POWER BI DATA EXPORT
# ==========================================

st.markdown("---")

st.header("📊 Microsoft Power BI Integration")

st.write(
    "Download the processed student analytics dataset "
    "and import it into Microsoft Power BI Desktop."
)

st.subheader("📋 Power BI Dataset Preview")

st.dataframe(
    analytics_df,
    use_container_width=True
)


# CSV EXPORT

csv_data = analytics_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Power BI CSV Dataset",
    data=csv_data,
    file_name="Smart_College_Analytics.csv",
    mime="text/csv",
    use_container_width=True
)


# EXCEL EXPORT

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
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)


# ==========================================
# 20. FOOTER
# ==========================================

# ==========================================
# 20. FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div style="background:linear-gradient(120deg,#312e81,#5b21b6);
padding:20px;border-radius:15px;text-align:center;">

<h3 style="color:white;">
🎓 AI Smart College Companion
</h3>

<p style="color:#ddd6fe;">
Collaborative Multi-Agent System
</p>

<p style="color:#c4b5fd;font-size:12px;">
Smart Analytics | AI Recommendations | Student Success
</p>

</div>
""", unsafe_allow_html=True)
