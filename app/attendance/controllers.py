import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.attendance.models import Attendance
import pymongo
import util
from datetime import date, datetime


class AttendanceManager(object):
    @classmethod
    def get_attendance(cls):
        from app import db

        data = list(db.classes.find())
        for classx in data:
            classx["_id"] = str(classx["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_attendance_by_student(cls, code):
        from app import db

        data = db.classes.find_one({"sr_code": code})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_attendance_by_class(cls, code):
        from app import db

        data = db.attendance.find_one({"class_code": code})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
    

    @classmethod
    def register_attendance(cls, code, body):
        from app import db
        current_class = db.classes.find_one({"code": code})
        if current_class:
            if current_class["expires_at"] < datetime.now():
                return {"message": "Class attendance has expired."}

            attended = db.attendance.find_one(
                {"class_code": code, "srcode": body.get("srcode")}
            )
            if attended:
                return {"message": "You have already attended this class."}

            clss = db.classes.find_one({"code": code})
            subject = db.subjects.find_one({"name": clss["subject_name"]})
            prof = db.prof.find_one({"prof_code": clss["prof_code"]})

            today = date.today()
            db.attendance.insert_one(
                {"class_code": code, "srcode": body.get("srcode"), "subject": subject["name"], "date": today.strftime("%B %d, %Y"), "prof_name": prof["name"]}
            )
            return {"message": "Class attendance has been registered"}

        else:
            return {"message": "Invalid class code was scanned"}
