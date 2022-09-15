import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.classes.models import Classes
import pymongo
import util


class ClassManager(object):
    @classmethod
    def get_classes(cls):
        from app import db

        data = list(db.classes.find())
        for classx in data:
            classx["_id"] = str(classx["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_classes_by_code(cls, code):
        from app import db

        data = db.classes.find_one({"class_code": code})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
