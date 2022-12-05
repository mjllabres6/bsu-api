import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.attendance.models import Attendance
from app.students.controllers import StudentManager
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

        data = list(db.attendance.find({"class_code": code}))
        for attendance in data:
            attendance["_id"] = str(attendance["_id"])
            sr_code = attendance.get('sr_code')

            print(sr_code)
            student = StudentManager.get_student_by_code(sr_code)
            attendance["name"] = f'{student["first_name"]} {student["last_name"]}'

        return jsonify({"data": data})

    @classmethod
    def register_attendance(cls, code, body):
        from app import db
        import pytz

        student = db.students.find_one({"sr_code": code})

        current_class = db.classes.find_one({"code": code})
        if current_class:
            if current_class["expires_at"] < datetime.now():
                return {"message": "Class attendance has expired."}

            attended = db.attendance.find_one(
                {"class_code": code, "sr_code": body.get("sr_code")}
            )
            if attended:
                return {"message": "You have already attended this class."}

            clss = db.classes.find_one({"code": code})
            subject = db.subjects.find_one({"_id": ObjectId(clss["subject_id"])})
            prof = db.professors.find_one({"_id": subject["prof_id"]})


            tz = pytz.timezone("Singapore") 
            today = datetime.now(tz)
            db.attendance.insert_one(
                {
                    "class_code": code,
                    "sr_code": body.get("sr_code"),
                    "subject": subject["name"],
                    "date": today.strftime("%B %d, %Y"),
                    "prof_name": prof["name"],
                    "section": student["section"]
                }
            )
            return {"message": "Class attendance has been registered"}

        else:
            return {"message": "Invalid class code was scanned"}
