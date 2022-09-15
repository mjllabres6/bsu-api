import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.subjects.models import Subjects
import pymongo
import util


class SubjectManager(object):
    @classmethod
    def get_subjects(cls):
        from app import db

        data = list(db.subjects.find())
        for subject in data:
            subject["_id"] = str(subject["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_subject_by_id(cls, id):
        from app import db

        data = db.students.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
