from flask import Blueprint
from flask import jsonify, make_response, request
from app.subjects.controllers import SubjectManager
from flask import url_for

module = Blueprint("subjects", __name__)


@module.route("/subjects", methods=["GET"])
def get_subjects():
    res = SubjectManager.get_subjects()
    return make_response(res)

@module.route("/subjects", methods=["POST"])
def get_prof_subjects():
    json_data = request.get_json(force=True)
    res = SubjectManager.get_prof_subjects(json_data)
    return make_response(res)

@module.route("/subjects/<sr_code>", methods=["GET"])
def get_student_subjects(sr_code):
    res = SubjectManager.get_student_subjects(sr_code)
    return make_response(res)

