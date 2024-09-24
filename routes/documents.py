from bson import ObjectId
from flask import Blueprint, app, jsonify, request
from pymongo import MongoClient

dbconnection = MongoClient('mongodb://localhost:27017/')
db = dbconnection['enterprise']

documents_bp = Blueprint('documents', __name__)


@documents_bp.route('/api/documents/<collection_name>', methods=['GET'])
def get_documents(collection_name):
    try:
        documents = list(db[collection_name].find())
        for doc in documents:
            # Convert ObjectId to string for JSON serialization
            doc['_id'] = str(doc['_id'])
        return jsonify({'documents': documents}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/api/documents/<collection_name>/<doc_id>', methods=['PUT'])
def update_document(collection_name, doc_id):
    try:
        updated_data = request.json
        result = db[collection_name].update_one(
            {'_id': ObjectId(doc_id)}, {'$set': updated_data})
        if result.modified_count == 1:
            return jsonify({'message': 'Документ оновлено успішно'}), 200
        else:
            return jsonify({'message': 'Документ не знайдено або немає змін'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/api/documents/<collection_name>/<doc_id>', methods=['DELETE'])
def delete_document(collection_name, doc_id):
    try:
        result = db[collection_name].delete_one({'_id': ObjectId(doc_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Документ видалено успішно'}), 200
        else:
            return jsonify({'message': 'Документ не знайдено'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
