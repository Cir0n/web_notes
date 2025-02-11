from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.controllers.auth_controller import AuthController


class AuthViews:
    """
    AuthViews handles the routes and views for authentication-related
      operations.
    """

    def __init__(self):
        """
        Initializes the AuthViews with the necessary controller and
        registers the routes.
        """
        self.auth_bp = Blueprint("auth_bp", __name__)
        self.controller = AuthController()
        self.register_routes()

    def register_routes(self):
        """
        Registers the routes for authentication-related operations.
        """

        @self.auth_bp.route("/", methods=["GET"])
        def home():
            """
            Redirects to the login page.

            :return: Redirect to the login page.
            """
            return redirect(url_for("auth_bp.login"))

        @self.auth_bp.route("/login", methods=["GET", "POST"])
        def login():
            """
            Handles the login process.

            :return: The rendered template for the login page or a redirect
            to the appropriate dashboard.
            """
            if request.method == "POST":
                username = request.form.get("username")
                password = request.form.get("password")
                result = self.controller.login(username, password)

                if "error" in result:
                    return render_template(
                        "auth/login.html", message=result["error"]
                    )
                if result["role"] == "student":
                    return redirect(url_for("student_bp.student_dashboard"))
                if result["role"] == "teacher":
                    return redirect(url_for("teacher_bp.teacher_dashboard"))
                if result["role"] == "admin":
                    return redirect(url_for("admin_bp.admin_dashboard"))

                return redirect("/profile")
            return render_template("auth/login.html")

        @self.auth_bp.route("/logout")
        def logout():
            """
            Handles the logout process.

            :return: Redirect to the login page.
            """
            self.controller.logout()
            return redirect(url_for("auth_bp.login"))

        @self.auth_bp.route("/profile")
        def profile():
            """
            Renders the profile page.

            :return: The rendered template for the profile page or a message
            indicating no user is logged in.
            """
            if "user_id" in session:
                return f"""User {session["user_id"]} is logged
                in as {session["role"]}"""
            return "No user logged in"
