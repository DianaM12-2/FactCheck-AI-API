from flask import Flask
from flask_cors import CORS
from .routes.claims import claims_bp
from .routes.factcheck import factcheck_bp
from .routes.health import health_bp


def create_app(config=None):
    """Application factory pattern for Flask."""
    app = Flask(__name__)

    # Default config
    app.config.update(
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    )

    if config:
        app.config.update(config)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(claims_bp, url_prefix="/api/v1/claims")
    app.register_blueprint(factcheck_bp, url_prefix="/api/v1/factcheck")

    return app
