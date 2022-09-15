import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.grades.models import Grades
import pymongo
import util


class GradeManager(object):
    @classmethod
    def get_grades(cls):
        from app import db

        data = list(db.grades.find())
        for grade in data:
            grade["_id"] = str(grade["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_grades_by_sr_code(cls, code):
        from app import db

        data = db.grades.find_one({"sr_code": code})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
