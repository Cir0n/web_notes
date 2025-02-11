import os
import secrets

from dotenv import load_dotenv
from flask import Flask, render_template, request, session

from app.extensions import bcrypt
from app.views.admin_view import AdminViews
from app.views.auth_views import AuthViews
from app.views.student_views import StudentViews
from app.views.teacher_views import TeacherViews

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

    @app.before_request
    def add_csrf_token():
        """
        Ajoute un token CSRF unique dans la session si inexistant.
        Cela empêche les attaques CSRF en exigeant un token valide pour chaque
        requête POST, PUT, DELETE.
        """
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(
                32
            )  # Génération du token CSRF
            session.modified = True

    @app.before_request
    def csrf_protect():
        """
        Vérifie la présence du token CSRF pour toutes les requêtes sensibles.
        Empêche toute requête sans un token CSRF valide.
        """
        if request.method in ["POST", "PUT", "DELETE"]:
            token = request.form.get("csrf_token") or request.headers.get(
                "X-CSRFToken"
            )
            if not token or token != session.get("csrf_token"):
                return render_template("errors/csrf_error.html"), 403

    bcrypt.init_app(app)

    student_views = StudentViews()
    teacher_views = TeacherViews()
    auth_views = AuthViews()
    admin_views = AdminViews()

    app.register_blueprint(student_views.student_bp, url_prefix="/students")
    app.register_blueprint(teacher_views.teacher_bp, url_prefix="/teachers")
    app.register_blueprint(auth_views.auth_bp, url_prefix="/")
    app.register_blueprint(admin_views.admin_bp, url_prefix="/admin")

    return app
