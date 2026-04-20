"""
Application Factory - Initializes Flask app with all extensions and blueprints.
"""
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

mongo = PyMongo()
login_manager = LoginManager()


def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # ── Config ─────────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/school_management')
    app.config['WTF_CSRF_ENABLED'] = False  # Disable for API routes; enable per-form if needed

    # ── Extensions ─────────────────────────────────────────────────────────
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_page'
    login_manager.login_message_category = 'info'

    # ── Blueprints ─────────────────────────────────────────────────────────
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.teacher import teacher_bp
    from app.routes.student import student_bp
    from app.routes.timetable import timetable_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp,       url_prefix='/auth')
    app.register_blueprint(dashboard_bp,  url_prefix='/dashboard')
    app.register_blueprint(teacher_bp,    url_prefix='/teacher')
    app.register_blueprint(student_bp,    url_prefix='/student')
    app.register_blueprint(timetable_bp,  url_prefix='/timetable')
    app.register_blueprint(api_bp,        url_prefix='/api')

    # ── Index route ────────────────────────────────────────────────────────
    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    # ── User loader for Flask-Login ────────────────────────────────────────
    from app.models.user import load_user_by_id
    login_manager.user_loader(load_user_by_id)

    # ── Seed initial data ──────────────────────────────────────────────────
    with app.app_context():
        from app.utils.seeder import seed_if_empty
        seed_if_empty()

    return app
