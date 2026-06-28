import streamlit as st
import pandas as pd

from agents.attendance_agent import AttendanceAgent
from agents.performance_agent import PerformanceAgent
from agents.skill_agent import SkillAgent
from agents.job_agent import JobAgent
from agents.placement_agent import PlacementAgent
from agents.course_agent import CourseAgent
from agents.event_agent import EventAgent
from agents.resume_agent import ResumeAgent
# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="AI Smart College Companion",
    layout="wide"
)

st.title("🎓 AI Smart College Companion")
st.write("Collaborative Multi-Agent System")

# --------------------------------
# Upload Student Database
# --------------------------------
st.header("📂 Upload Student Database")

uploaded_file = st.file_uploader(
    "Choose CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("✅ Student Database Uploaded Successfully!")
else:
    data = pd.read_csv("students.csv")

# --------------------------------
# Create Agent Objects
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
# Select Student
# --------------------------------
student = st.selectbox(
    "👨‍🎓 Select Student",
    data["Name"]
)

row = data[data["Name"] == student].iloc[0]

# --------------------------------
# Agent Outputs
# --------------------------------
attendance = attendance_agent.check_attendance(
    row["Attendance"]
)

performance = performance_agent.check_performance(
    row["Maths"],
    row["Python"],
    row["AI"]
)

strong_skills, missing_skills = skill_agent.analyze_skills(
    row["Python"],
    row["SQL"],
    row["Excel"],
    row["PowerBI"]
)

job = job_agent.recommend_job(
    strong_skills
)

placement = placement_agent.check_placement(
    row["Attendance"],
    row["CGPA"],
    row["Communication"]
)

courses = course_agent.recommend_courses(
    missing_skills
)

events = event_agent.recommend_events(
    strong_skills,
    placement
)
resume_score, improvements = resume_agent.calculate_score(
    row["Attendance"],
    row["CGPA"],
    row["Communication"],
    strong_skills,
    placement,
    missing_skills
)

# --------------------------------
# Dashboard
# --------------------------------
st.header("📋 Student Report")

col1, col2 = st.columns(2)

with col1:
    st.success(f"✅ Attendance : {attendance}")
    st.info(f"📈 Performance : {performance}")
    st.write(f"💼 Recommended Job : **{job}**")

with col2:
    st.success(f"🎯 Placement : {placement}")

    st.subheader("💻 Strong Skills")

    if len(strong_skills) == 0:
        st.warning("No Strong Skills")
    else:
        for skill in strong_skills:
            st.write("✅", skill)
st.subheader("📄 Resume Score")

st.metric(
    label="Overall Resume Score",
    value=f"{resume_score}/100"
)

st.progress(resume_score / 100)
st.subheader("🛠️ Areas to Improve")

if len(improvements) == 0:
    st.success("Excellent Resume! 🎉")
else:
    for item in improvements:
        st.write("❌", item)
# --------------------------------
# Missing Skills
# --------------------------------
st.subheader("❌ Missing Skills")

if len(missing_skills) == 0:
    st.success("🎉 No Missing Skills")
else:
    for skill in missing_skills:
        st.write("❌", skill)

# --------------------------------
# Recommended Courses
# --------------------------------
st.subheader("📚 Recommended Courses")

if len(courses) == 0:
    st.success("No Courses Required")
else:
    for course in courses:
        st.write("📖", course)

# --------------------------------
# Recommended Events
# --------------------------------
st.subheader("🎉 Recommended Events")

if len(events) == 0:
    st.info("No Events Available")
else:
    for event in events:
        st.write("🎯", event)

# --------------------------------
# Subject Marks Chart
# --------------------------------
st.subheader("📊 Subject Marks")

marks = pd.DataFrame({
    "Subject": ["Maths", "Python", "AI"],
    "Marks": [
        row["Maths"],
        row["Python"],
        row["AI"]
    ]
})

st.bar_chart(
    marks.set_index("Subject")
)