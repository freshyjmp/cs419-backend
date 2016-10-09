"""
Request DB Object
"""

import datetime

from backend.db import db
#from flask_sqlalchemy import UniqueConstraint

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    create_date = db.Column(db.DateTime)

    def __init__(self, url):
        self.url = url
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return 'Request(Build me a graph for %s !)' % (self.url)

