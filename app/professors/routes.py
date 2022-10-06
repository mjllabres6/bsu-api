from flask import Blueprint
from flask import jsonify, make_response, request
from app.professors.controllers import ProfessorManager
from flask import url_for

module = Blueprint("professors", __name__)


@module.route("/professors", methods=["GET"])
def get_professors():
    res = ProfessorManager.get_professors()
    return make_response(res)
