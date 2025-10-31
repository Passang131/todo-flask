from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app() -> Flask:
    load_dotenv()  # Load environment from .env when running locally

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///todo.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")
    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["DEBUG"] = app.config["ENV"] == "development"

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .auth import auth_bp  # noqa: WPS433
    from .routes import todos_bp  # noqa: WPS433
    from .pages import pages_bp  # noqa: WPS433

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(todos_bp, url_prefix="/api")
    app.register_blueprint(pages_bp)

    # Ensure tables exist for SQLite/simple setups without running migrations
    with app.app_context():
        db.create_all()

    

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


