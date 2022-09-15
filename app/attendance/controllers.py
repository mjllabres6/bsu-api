import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.attendance.models import Attendance
import pymongo
import util


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
