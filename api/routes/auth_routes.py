from flask import Blueprint, jsonify, redirect, request, session, render_template
from api.services.auth_service import AuthService
from api.routes.base_routes import BaseRoute 

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_route = BaseRoute(AuthService)

@auth_bp.route('/login', methods=['POST'])
def login():
    user = auth_route.service.login(request.form)
    if not user:
        return render_template('login.html', error='Invalid email or password')

    session['user_id'] = user.id
    session['role'] = user.role
    print(session)
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    user = auth_route.service.register(request.form)
    return jsonify({'status': 'success', 'message': 'Register successful', 'data': user}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return render_template('index.html')