from flask import Flask
from flask_cors import CORS, cross_origin



def create_app():
    # Create Flask Application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    #Database set up stuff
    from backend.db import db
    from backend.models import Request, Edge
    db.app = app
    db.init_app(app)
    db.create_all()

    #Using apimanager for some blueprints
    from backend.api import apimanager
    apimanager.init_app(app, flask_sqlalchemy_db=db)

    #Turn on CORS permissively for now
    CORS(app)

    @app.route('/')
    def hello():
        return "Hello dank wizard"

    return app
