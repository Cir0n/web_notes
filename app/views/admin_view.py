from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.controllers.class_controller import ClassController
from app.controllers.student_controller import StudentController
from app.controllers.subject_controller import SubjectController
from app.controllers.teacher_controller import TeacherController
from app.decorators import require_admin


class AdminViews:
    """
    AdminViews handles the routes and views for admin-related operations.
    """

    def __init__(self):
        """
        Initializes the AdminViews with the necessary controllers and
        registers the routes.
        """
        self.admin_bp = Blueprint("admin_bp", __name__)
        self.student_controller = StudentController()
        self.subject_controller = SubjectController()
        self.class_controller = ClassController()
        self.teacher_controller = TeacherController()
        self.register_routes()

    def register_routes(self):
        """
        Registers the routes for admin-related operations.
        """

        @self.admin_bp.route("/dashboard")
        @require_admin
        def admin_dashboard():
            """
            Renders the admin dashboard.

            :return: The rendered template for the admin dashboard.
            """
            return render_template("admin/dashboard.html")

        @self.admin_bp.route("/students")
        @require_admin
        def list_students():
            """
            Renders the list of students.

            :return: The rendered template for the list of students.
            """
            students = self.student_controller.list_students()
            options = self.subject_controller.get_options()
            languages = self.subject_controller.get_languages()
            return render_template(
                "admin/students.html",
                students=students,
                options=[o["name"] for o in options],
                languages=[language["name"] for language in languages],
            )

        @self.admin_bp.route("/add_student", methods=["GET", "POST"])
        @require_admin
        def add_student():
            """
            Handles the process of adding a new student.

            :return: The rendered template for adding a student or a redirect
            to the list of students.
            """
            classes = self.class_controller.get_all_classes()
            languages = self.subject_controller.get_languages()
            options = self.subject_controller.get_options()

            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                class_id = request.form.get("class")
                selected_languages = request.form.getlist("languages")
                selected_options = request.form.getlist("options")

                result = self.student_controller.create_student(
                    username,
                    password,
                    first_name,
                    last_name,
                    class_id,
                    selected_languages,
                    selected_options,
                )

                if "error" in result:
                    flash(result["error"])
                    return render_template(
                        "admin/add_student.html",
                        error=result["error"],
                        classes=classes,
                        languages=languages,
                        options=options,
                    )

                flash("etudiant ajouter avec succès")
                return redirect(url_for("admin_bp.list_students"))

            return render_template(
                "admin/add_student.html",
                classes=classes,
                languages=languages,
                options=options,
            )

        @self.admin_bp.route("/delete_student/<student_id>", methods=["POST"])
        @require_admin
        def delete_student(student_id):
            """
            Deletes a student by their ID.

            :param student_id: The ID of the student to be deleted.
            :return: Redirect to the list of students.
            """
            self.student_controller.delete_student(student_id)
            flash("Etudiant supprimé avec succès")
            return redirect(url_for("admin_bp.list_students"))

        # ----------------------------TEACHERS--------------------------------

        @self.admin_bp.route("/teachers")
        @require_admin
        def list_teachers():
            """
            Renders the list of teachers.

            :return: The rendered template for the list of teachers.
            """
            teachers = self.teacher_controller.list_teachers()
            return render_template("admin/teachers.html", teachers=teachers)

        @self.admin_bp.route("/add_teacher", methods=["GET", "POST"])
        @require_admin
        def add_teacher():
            """
            Handles the process of adding a new teacher.

            :return: The rendered template for adding a teacher or a redirect
            to the list of teachers.
            """
            subjects = self.subject_controller.get_all_subjects()
            classes = self.class_controller.get_all_classes()
            if request.method == "POST":
                print(request.form)
                username = request.form.get("username")
                password = request.form.get("password")
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                selected_classes = request.form.getlist("classes")
                selected_subjects = request.form.getlist("subjects")
                if not selected_subjects:
                    error = "❌ Vous devez sélectionner au moins une matière."
                    print(error)
                    flash(error, "danger")
                    return render_template(
                        "admin/add_teacher.html",
                        error=error,
                        classes=classes,
                        subjects=subjects,
                    )

                result = self.teacher_controller.create_teacher(
                    username,
                    password,
                    first_name,
                    last_name,
                    selected_classes,
                    selected_subjects,
                )

                if "error" in result:
                    flash(result["error"])
                    return render_template(
                        "admin/add_teacher.html",
                        error=result["error"],
                        subjects=subjects,
                        classes=classes,
                    )

                flash(result)
                return redirect(url_for("admin_bp.list_teachers"))

            return render_template(
                "admin/add_teacher.html", subjects=subjects, classes=classes
            )

        @self.admin_bp.route("/delete_teacher/<teacher_id>", methods=["POST"])
        @require_admin
        def delete_teacher(teacher_id):
            """
            Deletes a teacher by their ID.

            :param teacher_id: The ID of the teacher to be deleted.
            :return: Redirect to the list of teachers.
            """
            self.teacher_controller.delete_teacher(teacher_id)
            flash("Enseignant supprimé avec succès")
            return redirect(url_for("admin_bp.list_teachers"))
