from util.table import Table


class __Announcements:
    name = "announcements"
    columns = {
        "annc_id": str,
        "dept_id": str,
        "title": str,
        "header": str,
        "description": str,
        "created_at": str,
        "updated_at": str,
        "is_all_depts": bool,
    }

    optional = ["created_at", "updated_at"]


Announcements = __Announcements()
