import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.departments.models import Departments
import pymongo
import util


class DepartmentManager(object):
    @classmethod
    def get_departments(cls):
        from app import db
        print("GET DEPTS")
        data = list(db.departments.find())

        print(data)
        for dept in data:
            dept["_id"] = str(dept["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_department_by_id(cls, id):
        from app import db

        data = db.departments.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})
