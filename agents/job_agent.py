class JobAgent:

    def recommend_job(self, strong_skills):

        if "Python" in strong_skills and "SQL" in strong_skills and "Excel" in strong_skills:
            return "Data Analyst"

        elif "Python" in strong_skills and "Power BI" in strong_skills:
            return "Business Analyst"

        elif "Python" in strong_skills:
            return "Python Developer"

        else:
            return "Need More Skills"