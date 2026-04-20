"""
Application Factory - Initializes Flask app with all extensions and blueprints.
"""
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
import os
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# Load env vars
load_dotenv()

mongo = PyMongo()
login_manager = LoginManager()


def _mongo_timeout_ms(env_key: str, default: int = 3000) -> int:
    """Read timeout env vars safely and fallback to sane defaults."""
    try:
        value = int(os.getenv(env_key, str(default)))
        return value if value > 0 else default
    except (TypeError, ValueError):
        return default


def _build_mongo_uri(base_uri: str) -> str:
    """Ensure Mongo URI includes short timeouts for faster failure when DB is down."""
    parsed = urlparse(base_uri)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))

    query.setdefault('serverSelectionTimeoutMS', str(_mongo_timeout_ms('MONGO_SERVER_SELECTION_TIMEOUT_MS', 3000)))
    query.setdefault('connectTimeoutMS', str(_mongo_timeout_ms('MONGO_CONNECT_TIMEOUT_MS', 3000)))
    query.setdefault('socketTimeoutMS', str(_mongo_timeout_ms('MONGO_SOCKET_TIMEOUT_MS', 3000)))

    return urlunparse(parsed._replace(query=urlencode(query)))


def _db_unavailable_response():
    """Consistent fallback response when MongoDB is unreachable."""
    message = (
        'Database is unavailable. Start MongoDB and try again. '
        'Expected default URI: mongodb://localhost:27017/school_management'
    )

    wants_json = request.path != '/' and not request.path.startswith('/static/')
    if wants_json:
        return jsonify({'success': False, 'error': message}), 503

    return render_template('index.html', db_error=message), 503


def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # ── Config ─────────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key')
    app.config['MONGO_URI'] = _build_mongo_uri(
        os.getenv('MONGO_URI', 'mongodb://localhost:27017/school_management')
    )
    app.config['MONGO_CONNECT'] = False
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

    @app.route('/')
    def index():
        return render_template('index.html')

    # ── Global DB error handling ─────────────────────────────────────────────
    @app.errorhandler(ServerSelectionTimeoutError)
    @app.errorhandler(PyMongoError)
    def handle_mongo_errors(_error):
        return _db_unavailable_response()

    # ── User loader for Flask-Login ────────────────────────────────────────
    from app.models.user import load_user_by_id
    login_manager.user_loader(load_user_by_id)

    return app
