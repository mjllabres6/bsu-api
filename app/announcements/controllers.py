import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.announcements.models import Announcements
from app.students.controllers import StudentManager
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

        title = body.get("title") # 123
        description = body.get("description") # 12345
        dept = body.get("department") # CICS
        sr_code = body.get("sr_code") # CICSADMIN

        if title and description:
            try:
                db.announcements.insert_one(
                    {
                        "title": title, 
                        "department": dept, 
                        "description": description, 
                        "created_at": datetime.now(tzlocal()).strftime("%B %d, %Y %H:%M"), 
                        "created_by": sr_code 
                    }
                )
                return {"message": "Successfully created announcement"}
            except Exception as e:
                print(e)
                print(dir(e))
                return {"message": "Error while trying to create this announcement"}
    
    @classmethod
    def update_announcement(cls, body, announcement_id):
        from app import db

        admin = db.students.find_one({'sr_code': body.get('sr_code')})
        if not admin or (admin and not admin["is_admin"]):
            return {'message': 'You do not have permission to delete this'}

        title = body.get("title")
        description = body.get("description")
        new = {}
        if title:
            new.update({"title": title})

        if description:
            new.update({"description": description})
        
        print({"$set": new})

        db.announcements.update_one({'_id': ObjectId(announcement_id)}, {"$set": new})

    
    @classmethod
    def delete_announcement(cls, sr_code, announcement_id):
        from app import db

        admin = db.students.find_one({'sr_code': sr_code})
        if not admin or (admin and not admin["is_admin"]):
            return {'message': 'You do not have permission to delete this'}
        
        db.announcements.delete_one({'_id': ObjectId(announcement_id)})
