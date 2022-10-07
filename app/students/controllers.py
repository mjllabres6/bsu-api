import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.students.models import Students
import pymongo
import util


class StudentManager(object):
    @classmethod
    def get_students(cls):
        from app import db

        data = list(db.students.find())
        for student in data:
            student["_id"] = str(student["_id"])
            for subject in student["subjects"]:
                student["subjects"][student["subjects"].index(subject)] = str(subject)
        return jsonify({"data": data})

    @classmethod
    def get_student_by_id(cls, id):
        from app import db

        data = db.students.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_student_by_code(cls, code):
        from app import db

        student = db.students.find_one({"sr_code": code})
        student["_id"] = str(student["_id"])
        for subject in student["subjects"]:
                student["subjects"][student["subjects"].index(subject)] = str(subject)
        return student

    @classmethod
    def create_student(cls, body):
        from app import db

        user_body = util.validate_data(body, Students)

        timestamp = util.get_timestamp()
        user_body.update({"created": timestamp, "updated": timestamp})

        try:
            print(user_body)
            db.students.insert_one(user_body)
            return {"message": "Successfully created student record."}, 200
        except pymongo.errors.DuplicateKeyError:
            return {"message": "You have entered an existing record."}, 200
        except Exception as e:
            print(e)

            return {"message": "There was a problem creating student record"}, 200

    @classmethod
    def login_student(cls, body):
        from app import db

        user_body = {"sr_code": body.get("sr_code"), "password": body.get("password")}

        student = db.students.find_one(
            {"sr_code": user_body["sr_code"], "password": user_body["password"]}
        )
        if student:
            return {
                "message": "Found a match on a student record.",
                "name": f'{student["first_name"]} {student["last_name"]}',
            }, 200

        return {"message": "Invalid login credentials."}, 200
    

    @classmethod
    def get_student_liabilities(cls, sr_code):
        from app import db

        data = list(db.liabilities.find({"sr_code": sr_code}))
        print(data)
        for liab in data:
            data[data.index(liab)]["_id"] = str(liab["_id"])
        return jsonify({"data": data})
    
    @classmethod
    def get_student_curriculum(cls, sr_code):
        from app import db
        student = db.students.find({"sr_code": sr_code})

        curriculum = db.curriculum.find({"course": student["course"]})
        curriculum["_id"] = str(curriculum["_id"])
        return jsonify({"data": curriculum})
