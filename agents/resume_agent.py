class ResumeAgent:

    def calculate_score(
        self,
        attendance,
        cgpa,
        communication,
        strong_skills,
        placement,
        missing_skills
    ):

        score = 0

        if attendance >= 75:
            score += 20

        if cgpa >= 8:
            score += 20

        if communication in ["Good", "Excellent"]:
            score += 20

        if len(strong_skills) >= 3:
            score += 20

        if placement == "Eligible":
            score += 20

        improvements = []

        if attendance < 75:
            improvements.append("Improve Attendance")

        if cgpa < 8:
            improvements.append("Increase CGPA")

        if communication not in ["Good", "Excellent"]:
            improvements.append("Improve Communication")

        for skill in missing_skills:
            improvements.append(skill)

        return score, improvements