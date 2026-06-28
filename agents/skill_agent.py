class SkillAgent:

    def analyze_skills(self, python, sql, excel, powerbi):

        strong_skills = []
        missing_skills = []

        if python >= 80:
            strong_skills.append("Python")
        else:
            missing_skills.append("Python")

        if sql >= 70:
            strong_skills.append("SQL")
        else:
            missing_skills.append("SQL")

        if excel >= 70:
            strong_skills.append("Excel")
        else:
            missing_skills.append("Excel")

        if powerbi >= 70:
            strong_skills.append("Power BI")
        else:
            missing_skills.append("Power BI")

        return strong_skills, missing_skills