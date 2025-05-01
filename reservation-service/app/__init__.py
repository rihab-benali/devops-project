from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Load config from config.py

    db.init_app(app)
    migrate.init_app(app, db)  # <-- Required for `flask db` commands

    
    # Register Blueprints or routes
    from .routes import reservation_bp as routes_bp
    app.register_blueprint(routes_bp)

        
    # Register CLI commands
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database."""
        db.create_all()
        
        print("Initialized the database.")

    return app