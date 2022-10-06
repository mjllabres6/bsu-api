from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from app.subjects.controllers import SubjectManager
from flask import url_for

module = Blueprint("students", __name__)


@module.route("/students", methods=["GET"])
def get_students():
    res = StudentManager.get_students()
    return make_response(res)

@module.route("/students/<sr_code>", methods=["GET"])
def get_student_by_code(sr_code):
    res = StudentManager.get_student_by_code(sr_code)
    return make_response(res)


@module.route("/students", methods=["POST"])
def add_students():
    json_data = request.get_json(force=True)
    response, status = StudentManager.create_student(json_data)
    return make_response(jsonify(response)), status

@module.route("/students/login", methods=["POST"])
def login_student():
    json_data = request.get_json(force=True)
    res, status = StudentManager.login_student(json_data)
    return make_response(res), status


@module.route("/students/register", methods=["POST"])
def register_student():
    json_data = request.get_json(force=True)
    res, status = StudentManager.create_student(json_data)
    return make_response(res), status


@module.route("/students/<sr_code>/subjects", methods=["GET"])
def get_student_subjects(sr_code):
    res = SubjectManager.get_student_subjects(sr_code)
    return make_response(res)


@module.route("/students/<sr_code>/liab", methods=["GET"])
def get_student_liabilities(sr_code):
    res = StudentManager.get_student_liabilities(sr_code)
    return make_response(res)
