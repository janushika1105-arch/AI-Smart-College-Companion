import pandas as pd

from agents.attendance_agent import AttendanceAgent
from agents.performance_agent import PerformanceAgent
from agents.skill_agent import SkillAgent
from agents.job_agent import JobAgent
from agents.placement_agent import PlacementAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.course_agent import CourseAgent
from agents.event_agent import EventAgent

# Read dataset
data = pd.read_csv("students.csv")

# Create Agent Objects
attendance_agent = AttendanceAgent()
performance_agent = PerformanceAgent()
skill_agent = SkillAgent()
job_agent = JobAgent()
placement_agent = PlacementAgent()
course_agent = CourseAgent()
event_agent = EventAgent()
coordinator_agent = CoordinatorAgent()

# Process each student
for index, row in data.iterrows():

    # Attendance
    attendance = attendance_agent.check_attendance(
        row["Attendance"]
    )

    # Performance
    performance = performance_agent.check_performance(
        row["Maths"],
        row["Python"],
        row["AI"]
    )

    # Skills
    strong_skills, missing_skills = skill_agent.analyze_skills(
        row["Python"],
        row["SQL"],
        row["Excel"],
        row["PowerBI"]
    )

    # Job Recommendation
    job = job_agent.recommend_job(
        strong_skills
    )

    # Placement
    placement = placement_agent.check_placement(
        row["Attendance"],
        row["CGPA"],
        row["Communication"]
    )

    # Course Recommendation
    courses = course_agent.recommend_courses(
        missing_skills
    )

    # Event Recommendation
    events = event_agent.recommend_events(
        strong_skills,
        placement
    )

    # Final Report
    report = coordinator_agent.generate_report(
        attendance,
        performance,
        strong_skills,
        missing_skills,
        job,
        placement,
        courses,
        events
    )

    # Print Report
    print("\n==============================")
    print("Student :", row["Name"])

    for key, value in report.items():
        print(f"{key} : {value}")

    print("==============================")