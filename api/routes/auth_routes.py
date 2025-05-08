from flask import Blueprint, jsonify, request, session, render_template
from ..services.auth_service import AuthService
from .base_routes import BaseRoute 

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_route = BaseRoute(AuthService)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = auth_route.service.login(data)
    session['user_id'] = user['id']
    session['role'] = user['role']
    return jsonify({'status': 'success', 'message': 'Login successful', 'data': user}), 200

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = auth_route.service.register(data)
    return jsonify({'status': 'success', 'message': 'Register successful', 'data': user}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return render_template('index.html')