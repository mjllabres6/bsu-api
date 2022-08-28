from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("students", __name__)


@module.route("/students", methods=["GET"])
def get_students():
    res = StudentManager.get_students()
    return make_response(res)


@module.route("/students", methods=["POST"])
def add_students():
    json_data = request.get_json(force=True)
    response, status = StudentManager.create_student(json_data)
    return make_response(jsonify(response)), status


@module.route("/students/<id>", methods=["GET"])
def get_student_by_id(id):
    res = StudentManager.get_student_by_id(id)
    return make_response(res)


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
