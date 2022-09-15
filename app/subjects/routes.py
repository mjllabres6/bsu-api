from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("sections", __name__)


@module.route("/sections", methods=["GET"])
def get_sections():
    res = StudentManager.get_students()
    return make_response(res)
