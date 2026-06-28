class PlacementAgent:

    def check_placement(self, attendance, cgpa, communication):

        if attendance >= 75 and cgpa >= 7.5 and communication in ["Good", "Excellent"]:
            return "Eligible"

        return "Not Eligible"