class PerformanceAgent:

    def check_performance(self, maths, python, ai):

        average = (maths + python + ai) / 3

        if average >= 70:
            return "Good Performance"

        return "Need Improvement"