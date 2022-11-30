from flask import Blueprint
from flask import jsonify, make_response, request
from app.announcements.controllers import AnnouncementManager
from flask import url_for

module = Blueprint("announcements", __name__)


@module.route("/announcements", methods=["GET"])
def get_announcements():
    res = AnnouncementManager.get_announcements()
    return make_response(res)


@module.route("/announcements/<dept>", methods=["GET"])
def get_announcements_by_dept(dept):
    res = AnnouncementManager.get_announcements_by_dept(dept)
    return make_response(res)


@module.route("/announcements", methods=["POST"])
def create_announcement():
    json_data = request.get_json(force=True)
    res = AnnouncementManager.create_announcement(json_data)
    return make_response(jsonify(res))


@module.route("/announcements/<announcement_id>", methods=["PATCH"])
def update_announcement_by_id(announcement_id):
    json_data = request.get_json(force=True)
    AnnouncementManager.update_announcement(json_data, announcement_id)
    return make_response({'message': 'Successfully updated announcement'})

@module.route("/announcements/<announcement_id>/<sr_code>", methods=["DELETE"])
def delete_announcement_by_id(announcement_id, sr_code):
    AnnouncementManager.delete_announcement(sr_code, announcement_id)
    return make_response({'message': 'Successfully deleted announcement'})