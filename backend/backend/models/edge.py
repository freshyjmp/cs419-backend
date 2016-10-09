"""
Edge DB Object
"""

import datetime

from backend.db import db
#from flask_sqlalchemy import UniqueConstraint

class Edge(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request = db.Column(db.Integer, db.ForeignKey('request.id'))
    src_url = db.Column(db.String(1024))
    dst_url = db.Column(db.String(1024))
    create_date = db.Column(db.DateTime)

    db.UniqueConstraint('request','src_url','dst_url', name="_request_src_dst_uc")

    def __init__(self, request, src_url, dst_url):
        self.request = request
        self.src_url = src_url
        self.dst_url = dst_url
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return 'Edge([request: %d] %s ----> %s)' % (self.request, self.src_url, self.dst_url)

