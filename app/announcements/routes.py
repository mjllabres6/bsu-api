from flask import Blueprint
from flask import jsonify, make_response, request
from app.announcements.controllers import AnnouncementManager
from flask import url_for

module = Blueprint("announcements", __name__)


@module.route("/announcements", methods=["GET"])
def get_announcements():
    res = AnnouncementManager.get_announcements()
    return make_response(res)
