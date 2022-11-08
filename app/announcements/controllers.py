import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.announcements.models import Announcements
import pymongo
import util
from datetime import datetime
from dateutil.tz import tzlocal
import pytz

class AnnouncementManager(object):
    @classmethod
    def get_announcements(cls):
        from app import db

        data = list(db.announcements.find())
        for announcement in data:
            announcement["_id"] = str(announcement["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_announcements_by_dept(cls, dept):
        from app import db

        data = list(db.announcements.find({"department": dept}))
        for dept in data:
            dept["_id"] = str(dept["_id"])
        return jsonify({"data": data})
    
    @classmethod
    def create_announcement(cls, body):
        from app import db

        title = body.get("title")
        description = body.get("description")
        dept = body.get("department")
        sr_code = body.get("sr_code")
        if title and description:
            try:
                db.announcements.insert_one({"title": title, "department": dept, "description": description, "created_at": datetime.now(tzlocal()).strftime("%B %d, %Y %H:%M"), "created_by": sr_code })
                return {"message": "Successfully created announcement"}
            except Exception as e:
                print(e)
                print(dir(e))
                return {"message": "Error while trying to create this announcement"}
