from flask import Blueprint, jsonify, request
from ..services.user_service import UserService
from .base_routes import BaseRoute

user_bp = Blueprint('user', __name__, url_prefix='/api/users')
user_route = BaseRoute(UserService)

@user_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = user_route.service.get_all_users()
        return jsonify({'status': 'success', 'data': users}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = user_route.service.get_user_by_id(id)
        return jsonify({'status': 'success', 'data': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "User not found" else 500

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        user = user_route.service.update_user(id, data)
        return jsonify({'status': 'success', 'message': 'User updated successfully', 'data': user}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "User not found" else 400 if str(e) == "No fields to update" else 500

@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user_route.service.delete_user(id)
        return jsonify({'status': 'success', 'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "User not found" else 500
