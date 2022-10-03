from flask import Blueprint
from flask import jsonify, make_response, request
from app.students.controllers import StudentManager
from flask import url_for

module = Blueprint("announcements", __name__)


@module.route("/announcements", methods=["GET"])
def get_announcements():
    res = StudentManager.get_announcements()
    return make_response(res)
