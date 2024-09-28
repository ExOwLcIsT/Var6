from flask import Blueprint, jsonify, request
from pymongo import MongoClient

from decorators.access_controls import access_required

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


@collections_bp.route('/collections/<collection_name>/update_column', methods=['PUT'])
@access_required("admin")
def update_column(collection_name):

    data = request.json
    old_column_name = data.get('oldColumnName')
    new_column_name = data.get('newColumnName')

    if not old_column_name or not new_column_name:
        return jsonify({"error": "Назва старої та нової колонки є обов'язковими"}), 400

    if old_column_name == "_id":
        return jsonify({"error": "Не можна змінювати колонку _id"}), 400

    try:
        collection = db[collection_name]

        collection.update_many(
            {}, {'$rename': {old_column_name: new_column_name}})

        return jsonify({"message": f"Колонку '{old_column_name}' змінено на '{new_column_name}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@collections_bp.route('/collections/<collection_name>/delete_column', methods=['DELETE'])
@access_required("admin")
def delete_column(collection_name):
    data = request.json
    column_name = data.get('columnName')

    if not column_name:
        return jsonify({"error": "Назва колонки є обов'язковою"}), 400

    if column_name == "_id":
        return jsonify({"error": "Не можна видалити поле _id"}), 400
    try:
        collection = db[collection_name]

        collection.update_many({}, {'$unset': {column_name: ""}})

        return jsonify({"message": f"Колонку '{column_name}' успішно видалено"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
@access_required("owner")
def delete_collection(collection_name):
    try:
        db.drop_collection(collection_name)
        return jsonify({'message': f'Колекція {collection_name} видалена успішно'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@collections_bp.route('/collections/<collection_name>', methods=['POST'])
@access_required("owner")
def create_collection(collection_name):
    try:
        db[collection_name].insert_one({"placeholder": True})
        return jsonify({'message': f'Колекція {collection_name} створена успішно'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500