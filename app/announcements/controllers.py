import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.announcements.models import Announcements
import pymongo
import util


class AnnouncementManager(object):
    @classmethod
    def get_announcements_by_dept(cls, dept_id):
        from app import db

        data = list(db.announcements.find({"dept_id": dept_id}))
        for dept in data:
            dept["_id"] = str(dept["_id"])
        return jsonify({"data": data})
