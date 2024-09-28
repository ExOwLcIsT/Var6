from flask import Blueprint, jsonify
from pymongo import MongoClient

dbconnection = MongoClient('mongodb://localhost:27017/')
db = dbconnection['enterprise']

collections_bp = Blueprint('collections', __name__)


@collections_bp.route('/collections', methods=['GET'])
def get_all_collections():
    try:
        collections = db.list_collection_names()
        return jsonify(collections), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@collections_bp.route('/collections/<collection_name>', methods=['GET'])
def get_collection_data(collection_name):
    try:
        collection = db[collection_name]
        documents = list(collection.find({}))

        if not documents:
            return jsonify({"error": "Колекція порожня або не існує"}), 404

        fields = list(documents[0].keys())
        for document in documents:
            for field in fields:
                if (type(document[field]).__name__ == "ObjectId"):
                    document[field] = str(document[field])

        example_document = {field: "" for field in fields}

        response = {
            "collection_name": collection_name,
            "fields": fields,
            "documents": documents,
            "exampleDocument": example_document  # Add the example document to the response
        }

        return jsonify(response), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@collections_bp.route('/collections/<collection_name>', methods=['DELETE'])
def delete_collection(collection_name):
    try:
        db.drop_collection(collection_name)
        return jsonify({'message': f'Колекція {collection_name} видалена успішно'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@collections_bp.route('/collections/<collection_name>', methods=['POST'])
def create_collection(collection_name):
    try:
        db[collection_name].insert_one({"placeholder": True})
        return jsonify({'message': f'Колекція {collection_name} створена успішно'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
