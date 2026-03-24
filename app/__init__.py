from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.lists import lists_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(lists_bp)
    app.register_blueprint(tasks_bp)

    @app.route("/")
    def index():
        return jsonify({
            "name": "To-Do List API",
            "endpoints": {
                "lists": "/api/lists",
                "tasks": "/api/lists/<list_id>/tasks",
            },
        })

    return app
