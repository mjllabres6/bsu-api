from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("professors", __name__)


@module.route("/professors", methods=["GET"])
def get_professors():
    res = StudentManager.get_students()
    return make_response(res)
