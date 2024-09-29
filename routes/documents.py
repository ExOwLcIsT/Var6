from bson import ObjectId
from flask import Blueprint, app, jsonify, request
from pymongo import MongoClient

from decorators.access_controls import access_required

dbconnection = MongoClient('mongodb://localhost:27017/')
db = dbconnection['enterprise']

documents_bp = Blueprint('documents', __name__)


@documents_bp.route('/documents/<collection_name>', methods=['GET'])
def get_documents(collection_name):
    try:
        documents = list(db[collection_name].find())
        for doc in documents:
            for key in doc.keys():
                if (type(doc[key]).__name__ == "ObjectId"): 
                    doc[key] = str(doc[key])
        return jsonify({'documents': documents}), 200
    except Exception as e:
        print (e)
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/documents/<collection_name>', methods=['POST'])
@access_required("operator")
def create_document(collection_name):
    try:
        db[collection_name].insert_one(request.json)
        return jsonify({'message': 'Документ додано успішно'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/documents/<collection_name>/<doc_id>', methods=['PUT'])
@access_required("operator")
def update_document(collection_name, doc_id):
    try:
        updated_data = request.json
        updated_data['_id'] = ObjectId(updated_data['_id'])
        result = db[collection_name].update_one(
            {'_id': ObjectId(doc_id)}, {'$set': updated_data})
        if result.modified_count == 1:
            return jsonify({'message': 'Документ оновлено успішно'}), 200
        else:
            return jsonify({'message': 'Документ не знайдено або немає змін'}), 404
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/documents/<collection_name>/<doc_id>', methods=['DELETE'])
@access_required("operator")
def delete_document(collection_name, doc_id):
    try:
        result = db[collection_name].delete_one({'_id': ObjectId(doc_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Документ видалено успішно'}), 200
        else:
            return jsonify({'message': 'Документ не знайдено'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
