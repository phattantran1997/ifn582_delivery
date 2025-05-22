from flask import Blueprint, flash, redirect, request, session, render_template, url_for
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
        flash('invalid email or passsword', 'error')
        return render_template('login.html')
    # validate password
    if not auth_route.service.verify_password(request.form['password'], user.password):
        flash('invalid email or passsword', 'error')
        return render_template('login.html')

    session['user_id'] = user.id
    session['role'] = user.role.name
    return redirect(url_for('main.home'))

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    if request.form['password'] != request.form['confirm_password']:
        flash('Passwords do not match', 'error')
        return render_template('register.html')

    if auth_route.service.exist(request.form['email']):
        flash('Email already exists', 'error')
        return render_template('register.html')

    user = auth_route.service.register(request.form)
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('main.home'))
