from util.table import Table


class __Departments:
    name = "departments"
    columns = {
        "dept_code": str,
        "dept_name": str,
        "created_at": str,
        "updated_at": str,
    }

    optional = ["created_at", "updated_at"]


Departments = __Departments()
