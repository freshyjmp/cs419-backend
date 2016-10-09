import requests

from flask import Flask

from backend.db import db
from backend.models import Request, Edge
from backend.api import apimanager

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

# Instantiate Application
app = Flask(__name__)


# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
## Tell db what app we are using 
db.app = app
## Make the tables
db.init_app(app)
db.create_all()


#Create some dummy data
r1 = Request('http://www.google.com')
db.session.add(r1)
db.session.commit()

# Start API-Manager
apimanager.init_app(app, flask_sqlalchemy_db=db)


# This is a decorator
@app.route('/')
def hello():
    return "Hello wizzurd"



# Start application
if __name__ == '__main__':
    app.run()
