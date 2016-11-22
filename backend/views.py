from flask import Blueprint,jsonify
from backend.app import create_app
from backend.db import db
from backend.models import Edge
from sqlalchemy import and_

results = Blueprint('results_page', __name__)
@results.route('/api/results/<int:request_id>')
def show_result(request_id):
    query_result = Edge.query.filter_by(request=request_id).all()
    print("got this many rows %d" % len(query_result))
    for index, row in enumerate(query_result):
        row_as_dict = row.as_dict()
        query_result[index] = row_as_dict
    return jsonify(rows=len(query_result),edges=query_result)

@results.route('/api/results/<int:request_id>/<int:row_number>')
def show_chunked_result(request_id, row_number):
    query_result = Edge.query.filter(and_(Edge.request == request_id,
      Edge.id > row_number)).limit(1000).all()
    print("RequestId:%d, starting from Id:%d, getting %d rows" % (request_id, row_number, len(query_result)))
    for index, row in enumerate(query_result):
        row_as_dict = row.as_dict()
        query_result[index] = row_as_dict
    return jsonify(rows=len(query_result),edges=query_result)
