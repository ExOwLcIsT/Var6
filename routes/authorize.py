from flask import Blueprint, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['enterprise']
authorize_bp = Blueprint('authorize', __name__)


@authorize_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    access_rights = data.get('access_rights')
    if len(password) < 8 or len(password) > 16:
        return jsonify({'error': 'Пароль має бути від 8 до 16 символів'}), 400
    db.Keys.insert_one(
        {'username': username, 'password': password, 'access_rights': access_rights})

    return jsonify({'message': 'Користувача успішно зареєстровано!'}), 201


@authorize_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if len(password) < 8 or len(password) > 16:
        return jsonify({'error': 'Пароль має бути від 8 до 16 символів'}), 400

    user = db.Keys.find_one({'username': username})
    print(user)
    print(password)
    if user and (user['password'] == password):
        return jsonify({'message': 'Вхід успішний!'}), 200

    return jsonify({'error': 'Неправильне ім`я користувача або пароль'}), 401


@authorize_bp.route('/login/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.json
        username = data.get('username')

        if not username:
            return jsonify({'error': 'Необхідно вказати логін'}), 400

        user = db.Keys.find_one({'username': username})

        if not user:
            return jsonify({'error': 'Користувач не знайдений'}), 404

        password = user.get('password')

        if not password:
            return jsonify({'error': 'Пароль не знайдений'}), 404

        return jsonify({'password': password}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
