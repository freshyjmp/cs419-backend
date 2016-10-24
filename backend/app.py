from flask import Flask



def create_app():
    # Create Flask Application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    #
    from backend.db import db
    from backend.models import Request, Edge
    db.app = app
    db.init_app(app)
    db.create_all()

    #
    from backend.api import apimanager
    apimanager.init_app(app, flask_sqlalchemy_db=db)
    @app.route('/')
    def hello():
        return "Hello dank wizard"

    return app
