from flask import Blueprint
from flask import jsonify, make_response, request
from app.departments.controllers import DepartmentManager
from flask import url_for

module = Blueprint("departments", __name__)


@module.route("/departments", methods=["GET"])
def get_departments():
    res = DepartmentManager.get_departments()
    return make_response(res)
