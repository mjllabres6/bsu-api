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
    def get_professor_by_id(cls, id):
        from app import db

        data = db.professors.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
