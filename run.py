from flask import Flask
from views import main_blueprint
from flask_mysqldb import MySQL

app = Flask(__name__)

# Register the blueprint from views.py
app.register_blueprint(main_blueprint)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'delivery_service'

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True) 