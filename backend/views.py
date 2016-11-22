from flask import Blueprint,jsonify
from backend.app import create_app
from backend.db import db
from backend.models import Edge


results = Blueprint('results_page', __name__)
@results.route('/api/results/<int:request_id>')
def show_result(request_id):
    query_result = Edge.query.filter_by(request=request_id).all()
    print("request id %d got this many rows %d" % (request_id, len(query_result)))
    for index, row in enumerate(query_result):
        row_as_dict = row.as_dict()
        query_result[index] = row_as_dict
    return jsonify(rows=len(query_result),edges=query_result)


