class CoordinatorAgent:

    def generate_report(
        self,
        attendance,
        performance,
        strong_skills,
        missing_skills,
        job,
        placement,
        courses,
        events
    ):

        report = {}

        report["Attendance"] = attendance
        report["Performance"] = performance
        report["Strong Skills"] = strong_skills
        report["Missing Skills"] = missing_skills
        report["Recommended Job"] = job
        report["Placement"] = placement
        report["Recommended Courses"] = courses
        report["Recommended Events"] = events
        
        return report