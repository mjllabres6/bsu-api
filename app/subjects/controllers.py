import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.subjects.models import Subjects
from app.students.controllers import StudentManager
from app.professors.controllers import ProfessorManager
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

        data = db.subjects.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        data["prof_id"] = str(data["prof_id"])
        return data
    
    @classmethod
    def get_student_subjects(cls, sr_code):
        student = StudentManager.get_student_by_code(sr_code)
        subjects = [] 
        for subject in student["subjects"]:
            subject = cls.get_subject_by_id(subject)
            print(subject)
            prof = ProfessorManager.get_professor_by_id(subject["prof_id"])

            subject.update({"professor": prof["name"]})
            subject.pop('_id')
            subject.pop('prof_id')
            subjects.append(subject)

        return jsonify({"subjects": subjects})
