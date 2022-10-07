import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.classes.models import Classes
import pymongo
import util
from io import BytesIO
import qrcode
import uuid
from datetime import date, datetime, timedelta


class ClassManager(object):
    @classmethod
    def create_class(cls, body):
        from app import db

        code = str(uuid.uuid4())
        today = date.today()
        subject_body = {
            "subject_name": body.get("subject_name"),
            "duration": body.get("duration"),
            "date": today.strftime("%B %d, %Y"),
            "prof_code": body.get("prof_code"),
        }

        expiry = datetime.now() + timedelta(hours=int(subject_body.pop("duration")))

        subject_body.update({"code": code, "expires_at": expiry})

        try:
            db.classes.insert_one(subject_body)
            return {"code": code}
        except Exception:
            return {"message": "There was a problem creating the class."}

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

    @classmethod
    def produce_qr(cls, id):

        buffer = BytesIO()

        img = qrcode.make(str(id))
        img.save(buffer)
        buffer.seek(0)
        return buffer

    @classmethod
    def get_student_count(cls, code):
        from app import db

        data = db.attendance.count_documents({"class_code": code})
        return {"count": data}
