class CourseAgent:

    def recommend_courses(self, missing_skills):

        courses = []

        if "Python" in missing_skills:
            courses.append("Python for Beginners")

        if "SQL" in missing_skills:
            courses.append("SQL Basics")

        if "Excel" in missing_skills:
            courses.append("Advanced Excel")

        if "Power BI" in missing_skills:
            courses.append("Power BI Essentials")

        return courses