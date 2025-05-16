# run.py
from flask import Flask
from api.routes.product_routes import product_bp
from api.routes.user_routes import user_bp
from api.routes.base_routes import main_bp
from api.routes.auth_routes import auth_bp
from api.routes.admin_routes import admin_bp
from api.routes.cart_routes import cart_bp
from utils.mysql_init import MySQLManager
from config import load_env_file    
import os

load_env_file()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
# Set secret key for session
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize MySQL singleton
MySQLManager.init_app(app)

# Register routes
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cart_bp)

if __name__ == '__main__':
    app.run(debug=True)
