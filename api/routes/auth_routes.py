from flask import Blueprint, jsonify, redirect, request, session, render_template
from api.services.auth_service import AuthService
from api.routes.base_routes import BaseRoute 

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_route = BaseRoute(AuthService)

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    user = auth_route.service.login(request.form)
    if not user:
        return render_template('login.html', error='Invalid email or password')
    # validate password
    if not auth_route.service.verify_password(request.form['password'], user.password):
        return render_template('login.html', error='Invalid email or password')

    session['user_id'] = user.id
    session['role'] = user.role
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    if request.form['password'] != request.form['confirm_password']:
        return render_template('register.html', error='Passwords do not match')

    if auth_route.service.exist(request.form['email']):
        return render_template('register.html', error='Email already exists')

    user = auth_route.service.register(request.form)
    return render_template('login.html', success='Register successful, please login')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return render_template('index.html')