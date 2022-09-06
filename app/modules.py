import os


def register():
    from app import app
    from app.students.routes import module as students_module
    from app.sections.routes import module as sections_module
    from app.subjects.routes import module as subjects_module
    from app.professors.routes import module as professors_module
    from app.grades.routes import module as grades_module
    from app.departments.routes import module as departments_module
    from app.announcements.routes import module as announcements_module

    modules = [
        students_module, 
        sections_module,
        subjects_module,
        professors_module,
        grades_module,
        departments_module,
        announcements_module
    ]
    
    for module in modules:
        app.register_blueprint(module, url_prefix="/bsu-api")
    