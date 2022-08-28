import os


def register():
    from app import app
    from app.students.routes import module as students_module
    app.register_blueprint(students_module, url_prefix="/bsu-api")
