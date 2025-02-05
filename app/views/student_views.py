from flask import Blueprint, render_template, session

from app.controllers.student_controller import StudentController
from app.decorators import require_student


class StudentViews:
    def __init__(self):
        self.student_bp = Blueprint("student_bp", __name__)
        self.controller = StudentController()
        self.register_routes()

    def register_routes(self):
        @self.student_bp.route("/me")
        @require_student
        def student_dashboard():  # TODO: Revoir les infos présente dans
            # le dashboard peut être ajouter un emploie du temps etc...
            student_id = session.get("user_id")

            if session.get("role") != "student":
                return render_template("errors/unauthorized.html")

            grades = self.controller.get_student_grades(student_id)
            subjects = self.controller.get_student_subject(student_id)

            return render_template(
                "student/dashboard.html",
                grades=grades,
                subjects=subjects,
                student_id=student_id,
            )

        @self.student_bp.route("/subject/<int:subject_id>")
        @require_student
        def student_subject_grades(subject_id):
            student_id = session.get("user_id")

            if session.get("role") != "student":
                return render_template("errors/unauthorized.html")

            subject = self.controller.get_subject_info(subject_id)
            grades = self.controller.get_student_grades_by_subject(
                student_id, subject_id
            )

            return render_template(
                "student/subject_grades.html", grades=grades, subject=subject
            )
