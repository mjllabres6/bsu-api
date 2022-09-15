from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("departments", __name__)


@module.route("/departments", methods=["GET"])
def get_departments():
    res = StudentManager.get_students()
    return make_response(res)
