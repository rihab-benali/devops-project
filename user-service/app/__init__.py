from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.kafka_consumer import start_consumer
start_consumer()


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Load config from config.py

    db.init_app(app)
    migrate.init_app(app, db)  # <-- Required for `flask db` commands

    

    # Register Blueprints or routes
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

        # Register CLI commands
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database."""
        db.create_all()
        
        # Add default roles if using Role model
        from .models import Role
        if not Role.query.first():
            db.session.add(Role(name='admin'))
            db.session.add(Role(name='user'))
            db.session.commit()
            print("Added default roles")
        
        print("Initialized the database.")

    return app

