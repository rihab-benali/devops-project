from app import create_app
from flask_migrate import Migrate
from app import db  # Make sure db is imported to work with Migrate
from flask.cli import with_appcontext
import click
from app.models import Room  # add your models here

app = create_app()
migrate = Migrate(app, db)

@click.command(name='init-db')
@with_appcontext
def init_db():
    db.create_all()
    click.echo('Initialized the database.')

app.cli.add_command(init_db)

if __name__ == "__main__":
    app.run()

