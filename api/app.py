import os

from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
import click

from models import db
from routes import api
from common.util import convert_keys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://{}:{}@{}/{}'.format(
                *[os.environ.get(var) for var in \
                        ['DBUSER', 'DBPASS', 'DBHOST', 'DBNAME']])

@app.before_request
def before_req():
    """
    Convert JSON keys from incoming request to snake case
    """
    if request.get_json(silent=True):
        convert_keys(request.get_json(), 'snake')

@app.after_request
def session_commit(response):
    """
    Commit database transaction on response
    """
    if response.status_code >= 400:
        return response
    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise
    finally:
        return response

CORS(app)

db.init_app(app)
api.init_app(app)

#
# CLI commands
#

@app.cli.command()
def initdb():
    """
    Initialize the database by creating the tables
    for the declared models
    """
    click.echo('Initializing the database...')
    try:
        db.create_all()
        click.echo('Done')
    except Exception as e:
        raise e


FLASK_DEBUG = os.environ.get('FLASK_DEBUG', None) or True
FLASK_HOST = os.environ.get('FLASK_HOST', None) or '127.0.0.1'
if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST)
