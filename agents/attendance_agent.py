class AttendanceAgent:

    def check_attendance(self, attendance):

        if attendance >= 75:
            return "Good Attendance"

        return "Low Attendance"