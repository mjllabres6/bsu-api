import json
from flask import jsonify
from bson.objectid import ObjectId
from http import HTTPStatus
from app.grades.models import Grades
import pymongo
from app.students.controllers import StudentManager
from app.subjects.controllers import SubjectManager
import util


class GradeManager(object):
    @classmethod
    def get_grades(cls):
        from app import db

        data = list(db.grades.find())
        for grade in data:
            grade["_id"] = str(grade["_id"])
        return jsonify({"data": data})

    @classmethod
    def get_grades_by_sr_code(cls, code):
        from app import db

        student = StudentManager.get_student_by_code(code)
        res = []
        for sy in student["sems"]:
            sems = [1, 2]
            for sem in sems:
                grades = list(
                    db.grades.find({"student_id": code, "sy": sy, "sem": sem})
                )
                if grades:
                    for grade in grades:
                        [grade.pop(key) for key in ["_id", "student_id", "sy", "sem"]]
                        grade["subject"] = SubjectManager.get_subject_by_id(
                            grade["subject"]
                        )["name"]
                        grade["grade"] = float(str(grade["grade"]))

                    res.append({"sem": f"{sy} - {sem}", "grades": grades})

        return jsonify(res)

    @classmethod
    def get_student_gwa(cls, code):
        from app import db
        from sklearn.linear_model import LinearRegression
        import numpy as np

        student = StudentManager.get_student_by_code(code)
        current_sem = db.active.find_one({"secret_key": "sheesh"})["current_sem"]
        previous_sem = db.active.find_one({"secret_key": "sheesh"})["prev_sem"]
        res = {}
        gwas = []
        for sy in student["sems"]:
            sems = [1, 2]
            grand_total = 0
            total_subjects = 0
            for sem in sems:
                grades = list(
                    db.grades.find({"student_id": code, "sy": sy, "sem": sem})
                )
                total = 0
                if grades:
                    print('SEM WITH GRADE')
                    for grade in grades:
                        total_subjects += 1
                        total += float(str(grade["grade"]))

                    grand_total += total
                    average = round(total / len(grades), 2)

                    gwas.append(average)

                    if current_sem == f"{sy} - {sem}":
                        res["current_sem"] = average
                    elif previous_sem == f"{sy} - {sem}":
                        res["previous_sem"] = average

            res["overall"] = round(grand_total / total_subjects, 2)

            avrs = ["overall", "current_sem", "previous_sem"]
            sum = 0
            for key in avrs:
                if key not in res:
                    avrs.pop(key)
                sum += res[key]

        y = np.array(gwas).reshape(-1,1)
        x = np.array([i for i in range(1, len(gwas) + 1)]).reshape(-1,1)

        to_predict_x = np.array([len(gwas) + 1]).reshape(-1,1)
        regsr=LinearRegression()
        regsr.fit(x,y)

        predicted_y = regsr.predict(to_predict_x)

        res["expected_gwa"] = round(predicted_y[0][0], 2)
        # res["expected_gwa"] = round(sum / len(avrs), 2)
            

        return jsonify(res)

    @classmethod
    def get_student_graph(cls, code):
        from app import db
        import matplotlib.pyplot as plt
        import numpy as np
        import io

        plt.switch_backend("agg")

        student = StudentManager.get_student_by_code(code)

        y_gwa = []
        x_sems = []

        for sy in student["sems"]:
            sems = [1, 2]
            for sem in sems:
                grades = list(
                    db.grades.find({"student_id": code, "sy": sy, "sem": sem})
                )

                if grades:
                    total = 0
                    for grade in grades:
                        total += float(str(grade["grade"]))

                    average = round(total / len(grades), 2)
                    y_gwa.append(average)
                    x_sems.append(f"{sy} - {sem}")
        y = np.array(y_gwa)
        x = np.array(x_sems)

        plt.plot(x, y, "r")
        plt.xlabel("SEM")
        plt.ylabel("GWA")
        plt.gca().invert_yaxis()
        # plt.show()  # show first chart

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)
        return buffer
