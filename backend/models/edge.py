"""
Edge DB Object
"""

import datetime

from backend.db import db
#from flask_sqlalchemy import UniqueConstraint

class Edge(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request = db.Column(db.Integer, db.ForeignKey('request.id'))
    visit_number = db.Column(db.Integer)
    src_url = db.Column(db.String(1024), nullable=False)
    dst_url = db.Column(db.String(1024), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    had_keyword = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)

    db.UniqueConstraint('request','src_url','dst_url','depth',
                        name="_request_src_dst_uc")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, visit_number, request, src_url, dst_url, depth, had_keyword=False):
        self.request = request
        self.visit_number = visit_number
        self.src_url = src_url
        self.dst_url = dst_url
        self.depth = depth
        self.had_keyword = had_keyword

        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return 'Edge([request: %d] %s ----> %s)' % (self.request,
                                                    self.src_url, self.dst_url)
