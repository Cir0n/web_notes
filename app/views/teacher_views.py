from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.controllers.student_controller import StudentController
from app.controllers.teacher_controller import TeacherController
from app.decorators import require_teacher


class TeacherViews:
    def __init__(self):
        self.teacher_bp = Blueprint("teacher_bp", __name__)
        self.controller = TeacherController()
        self.student_controller = StudentController()
        self.register_route()

    def register_route(self):
        @self.teacher_bp.route("/dashboard")
        @require_teacher
        def teacher_dashboard():
            teacher_id = session.get("user_id")
            classes = self.controller.get_teacher_classes(teacher_id)
            return render_template("teacher/dashboard.html", classes=classes)

        @self.teacher_bp.route("/class/<int:class_id>")
        @require_teacher
        def class_students(class_id):
            students = self.controller.get_student_classes(class_id)
            subjects = self.controller.get_teacher_subjects(
                session.get("user_id")
            )
            return render_template(
                "teacher/class_students.html",
                students=students,
                class_id=class_id,
                subjects=subjects,
            )

        @self.teacher_bp.route("/add_grade", methods=["POST"])
        @require_teacher
        def add_grade():
            teacher_id = session.get("user_id")
            student_id = request.form["student_id"]
            subject_id = request.form["subject_id"]
            grade = request.form["grade"]
            comment = request.form["comment"]

            self.controller.add_grade(
                teacher_id, student_id, subject_id, grade, comment
            )

            student_info = self.student_controller.get_student_info(student_id)
            class_id = student_info["class_id"] if student_info else None

            return redirect(
                url_for("teacher_bp.class_students", class_id=class_id)
            )

        @self.teacher_bp.route("/student/<int:student_id>")
        @require_teacher
        def student_grades(student_id):
            teacher_id = session.get("user_id")
            grades = self.controller.get_student_grades(teacher_id, student_id)
            student_info = self.student_controller.get_student_info(student_id)
            class_id = student_info["class_id"]

            return render_template(
                "teacher/student_grades.html",
                grades=grades,
                class_id=class_id,
                student_id=student_id,
            )

        @self.teacher_bp.route("/delete_grade", methods=["POST"])
        @require_teacher
        def delete_grade():
            teacher_id = session.get("user_id")
            grade_id = request.form["grade_id"]
            student_id = request.form.get("student_id")
            self.controller.delete_grade(teacher_id, grade_id)
            flash("Note supprimée avec succès !")

            return redirect(
                url_for("teacher_bp.student_grades", student_id=student_id)
            )
