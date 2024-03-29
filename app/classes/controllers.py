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
from app.subjects.controllers import SubjectManager
from app.students.controllers import StudentManager
import csv
from datetime import datetime
import pytz

class ClassManager(object):
    @classmethod
    def create_class(cls, body):
        from app import db

        code = str(uuid.uuid4())

        tz = pytz.timezone("Singapore") 
        today = datetime.now(tz)
        # today = date.today()

        subject_id = body.get("subject_id")

        if len(subject_id) not in [12, 24] or not SubjectManager.get_subject_by_id(
            ObjectId(subject_id)
        ):
            return {"message": "Error finding a subject with this id."}



        subject_body = {
            "subject_id": subject_id,
            "duration": body.get("duration"),
            "date": today.strftime("%B %d, %Y"),
            "section": body.get("section")
        }

        print(subject_body)

        expiry = datetime.now() + timedelta(minutes=30)
        print(expiry)
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
            print('hello')
            classx["_id"] = str(classx["_id"])
            print(classx)
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

    @classmethod
    def get_student_attendance(cls, srcode):
        from app import db

        data = list(db.attendance.find({"sr_code": srcode}))
        for attendance in data:
            attendance["_id"] = str(attendance["_id"])
        data.reverse()
        return {"results": data}

    @classmethod
    def get_prof_classes(cls, srcode):
        from app import db

        data = list(db.classes.find({"prof_code": srcode}))
        for attendance in data:
            attendance["_id"] = str(attendance["_id"])
        return {"results": data}
    
    @classmethod
    def get_classes_by_subject(cls, subject_id):
        from app import db 

        subject = SubjectManager.get_subject_by_id(subject_id)

        print(subject)

        if not subject:
            return {"message": "No subject has this id"}, 500

        classes = list(db.classes.find({"subject_id": subject["_id"]}, {'_id': False}))
        for classx in classes:
            classx["attendees"] = len(list(db.attendance.find({'class_code': classx['code']})))
        return {"classes": classes}
    
    @classmethod
    def delete_class(cls, code, api_key = None):
        from app import db
        if not api_key or api_key != "K9QPL55Fv9ly":
            return {"message": "unauthorized"}

        clxss = db.classes.find_one({"code": code})
        if clxss:
            db.classes.delete_one({"code": code})
            return {"message": "OK"}
        return {"message": "class doesn't exist"}

    @classmethod
    def export_as_excel(cls, code):
        from app import db
        import xlsxwriter

        # import io

        data = list(db.attendance.find({"class_code": code}))
        name = ""

        chosen_class = db.classes.find_one({"code": code})
        subject = db.subjects.find_one({"_id": ObjectId(chosen_class["subject_id"])})
        prof = db.professors.find_one({"_id": ObjectId(subject["prof_id"])})


        row = 0
        col = 0

        intro_lines = [prof["name"], subject["name"], chosen_class["section"], chosen_class["date"], " "]



        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold':True})
        for value in intro_lines:
            worksheet.write(row, col, value, bold)
            row+= 1

        worksheet.write(row, col, "LRN", bold)
        worksheet.write(row, col + 1, "NAME", bold)
        row += 1

        for student in data:
            st = StudentManager.get_student_by_code(student["sr_code"])
            name = f"{st['first_name']} {st['last_name']}"
            worksheet.write(row, col, student["sr_code"])
            worksheet.write(row, col + 1, name)
            row += 1

        workbook.close()
        buffer.seek(0)
        return buffer, f"{chosen_class['date']} - {chosen_class['section']} - {subject['name']}"
