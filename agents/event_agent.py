class EventAgent:

    def recommend_events(self, strong_skills, placement):

        events = []

        if placement == "Eligible":
            events.append("Campus Placement Drive")
        else:
            events.append("Resume Building Workshop")

        if "Python" in strong_skills:
            events.append("Python Coding Contest")

        if "Power BI" in strong_skills:
            events.append("Data Analytics Workshop")

        return events