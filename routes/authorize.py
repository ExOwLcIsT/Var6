from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
authorize_bp = Blueprint('authorize', __name__)

@authorize_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if len(password) < 8 or len(password) > 16:
        return jsonify({'error': 'Пароль має бути від 8 до 16 символів'}), 400

    hashed_password = generate_password_hash(password)
    db.Keys.insert_one({'username': username, 'password': hashed_password})

    return jsonify({'message': 'Користувача успішно зареєстровано!'}), 201


@authorize_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if len(password) < 8 or len(password) > 16:
        return jsonify({'error': 'Пароль має бути від 8 до 16 символів'}), 400

    user = db.Keys.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Вхід успішний!'}), 200

    return jsonify({'error': 'Неправильне ім\'я користувача або пароль'}), 401
