import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.sections.models import Sections
import pymongo
import util


class SectionManager(object):
    @classmethod
    def get_sections(cls):
        from app import db

        data = list(db.subjects.find())
        for section in data:
            section["_id"] = str(section["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_section_by_id(cls, id):
        from app import db

        data = db.sections.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
