from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("grades", __name__)


@module.route("/grades", methods=["GET"])
def get_grades():
    res = StudentManager.get_students()
    return make_response(res)
