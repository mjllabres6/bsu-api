from util.table import Table

class __Sections():
    name = "sections"
    columns = {
            "section_id": str,
            "section_code": str,
            "prof_id": str,
            "created_at": str,
            "updated_at": str,
    }

    optional = ["created_at", "updated_at"]



Sections = __Sections()
