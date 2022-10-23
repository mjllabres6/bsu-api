from flask import Blueprint, send_file
from flask import jsonify, make_response, request
from app.grades.controllers import GradeManager
from flask import url_for

module = Blueprint("grades", __name__)


@module.route("/grades", methods=["GET"])
def get_grades():
    res = GradeManager.get_students()
    return make_response(res)


@module.route("/grades/<code>", methods=["GET"])
def get_grades_by_student(code):
    res = GradeManager.get_grades_by_sr_code(code)
    return make_response(res)


@module.route("/grades/<code>/gwa", methods=["GET"])
def get_student_gwa(code):
    res = GradeManager.get_student_gwa(code)
    return make_response(res)


@module.route("/grades/<code>/graph", methods=["GET"])
def get_student_graph(code):
    res = GradeManager.get_student_graph(code)
    return send_file(res, mimetype="image/png")
