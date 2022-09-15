from asyncio.base_futures import _format_callbacks
from util.table import Table

class __Professors():
    name = "professors"
    columns = {
            "prof_id": str,
            "full_name": str,
            "gender": str,
            "phone": str,
            "created_at": str,
            "updated_at": str,
    }

    optional = ["created_at", "updated_at"]



Professors = __Professors()

