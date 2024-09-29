from flask import Blueprint, Response, jsonify, request
from bson import json_util, ObjectId
from pymongo import MongoClient
from datetime import datetime

dbconnection = MongoClient('mongodb://localhost:27017/')
db = dbconnection['enterprise']
requests_bp = Blueprint('requests', __name__)


@requests_bp.route('/query', methods=['POST'])
def run_query():
    data = request.json
    query_string = data.get('query', '')

    try:
        if isinstance(query_string, str) and query_string.startswith("db."):
            exec_env = {"db": db, "ObjectId": ObjectId, "datetime": datetime}
            exec(f"result = {query_string}", exec_env)

            result = exec_env['result']
            return Response(json_util.dumps(result), mimetype='application/json'), 200
        else:
            return jsonify({'error': 'Invalid query format'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400
