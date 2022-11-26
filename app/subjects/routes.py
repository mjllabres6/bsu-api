from flask import Blueprint
from flask import jsonify, make_response, request
from app.subjects.controllers import SubjectManager
from flask import url_for

module = Blueprint("subjects", __name__)


@module.route("/subjects", methods=["GET"])
def get_subjects():
    res = SubjectManager.get_subjects()
    return make_response(res)
