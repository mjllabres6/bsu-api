from util.table import Table

class __Grades():
    name = "grades"
    columns = {
            "grade_id": str,
            "subject_id": str,
            "student_id": str,
            "grade": str,
            "prof_id": str,
            "created_at": str,
            "updated_at": str,
    }

    optional = ["created_at", "updated_at"]


Grades = __Grades()
