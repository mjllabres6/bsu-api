from util import Table

class __Students():
    name = "students"
    columns = {
            "sr_code": str,
            "first_name": str,
            "last_name": str,
            "gender": str,
            "phone": str,
            "password": str,
            "section_id": int,
            "dept_id": int,
            "created_at": str,
            "updated_at": str,
    }

    optional = ["created_at", "updated_at"]



Students = __Students()
