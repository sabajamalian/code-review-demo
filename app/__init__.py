from flask import Flask, jsonify, render_template
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
        return render_template("index.html")

    return app
