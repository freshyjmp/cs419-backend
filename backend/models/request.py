"""
Request DB Object
"""

import datetime

from backend.db import db
#from flask_sqlalchemy import UniqueConstraint

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024), nullable=False)
    create_date = db.Column(db.DateTime)
    searchmode = db.Column(db.String(3), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    keyword = db.Column(db.String(255))

    def __init__(self, url, searchmode='DFS', depth=10, keyword=None):
        self.url = url
        self.keyword = keyword
        self.create_date = datetime.datetime.now()
        if searchmode not in ['DFS', 'BFS']:
            raise ValueError('searchmode provided was not valid. got %s' % (searchmode))
        else:
            self.searchmode = searchmode
        if int(depth) not in range(1,11):
            raise ValueError('depth provided was not valid. got %s' % (depth))
        else:
            self.depth = int(depth)

    def __repr__(self):
        return 'Request(Build me a graph for %s !)' % (self.url)

