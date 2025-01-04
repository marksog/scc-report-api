import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config.config import Config



db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

   # logging 
    logging.basicConfig(level=app.config['LOG_LEVEL'], format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from utils.error import init_error_handlers
    init_error_handlers(app)

    # using blueprints
    from .auth import auth_bp
    #from .admin import admin_bp
    from .routes import reports, summaries, dashboard

    app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(reports.reports_bp, url_prefix='/reports')
    app.register_blueprint(summaries.summaries_bp, url_prefix='/summaries')
    # app.register_blueprint(dashboard.dashboard_bp, url_prefix='/dashboard')

    return app