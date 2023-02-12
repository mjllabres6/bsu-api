from flask import make_response, request, Blueprint, send_file
from app.classes.controllers import ClassManager
from app.attendance.controllers import AttendanceManager

module = Blueprint("classes", __name__)


@module.route("/classes", methods=["POST"])
def create_class():
    json_data = request.get_json(force=True)
    res = ClassManager.create_class(json_data)
    return make_response(res)


@module.route("/classes/<class_id>", methods=["GET"])
def get_class_qr(class_id):

    res = ClassManager.produce_qr(class_id)

    return send_file(res, mimetype="image/gif")


@module.route("/classes/<code>", methods=["POST"])
def reg_qr(code):
    json_data = request.get_json(force=True)
    res = AttendanceManager.register_attendance(code, json_data)
    return make_response(res)




@module.route("/classes/<code>/count", methods=["GET"])
def get_student_count(code):
    res = ClassManager.get_student_count(code)
    return make_response(res)


@module.route("/subjects/<subject_id>/classes", methods=["GET"])
def get_classes_by_subject(subject_id):
    res = ClassManager.get_classes_by_subject(subject_id)
    return make_response(res)


@module.route("/classes/<code>/attendance", methods=["GET"])
def get_attendance_by_class(code):
    res = AttendanceManager.get_attendance_by_class(code)
    return make_response(res)


@module.route("/classes/<srcode>/attended", methods=["GET"])
def get_student_attendance(srcode):
    res = ClassManager.get_student_attendance(srcode)
    return make_response(res)


@module.route("/classes/<profcode>/conducted", methods=["GET"])
def get_prof_classes(profcode):
    res = ClassManager.get_prof_classes(profcode)
    return make_response(res)


@module.route("/classes/<code>/export", methods=["GET"])
def export_as_excel(code):
    res, filename = ClassManager.export_as_excel(code)
    return send_file(
        res, as_attachment=True, download_name=f"{filename}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@module.route("/classes/<code>/<api_key>", methods=["DELETE"])
def delete_class(code, api_key):
    res = ClassManager.delete_class(code, api_key)
    return res
