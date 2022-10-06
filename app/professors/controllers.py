import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.professors.models import Professors
import pymongo
import util


class ProfessorManager(object):
    @classmethod
    def get_professors(cls):
        from app import db

        data = list(db.professors.find())
        for prof in data:
            prof["_id"] = str(prof["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_professor_by_id(cls, prof_id):
        from app import db
        print(type(prof_id))
        print(prof_id)
        print({"_id": ObjectId(prof_id)})
        data = db.professors.find_one({"_id": ObjectId(prof_id)})
        data["_id"] = str(data["_id"])
        return data

