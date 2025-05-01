Delivery Service Web App

This is a simple web application for a delivery service using Flask and MySQL.

Requirements:
- Python 3.x
- Flask
- Flask-WTF
- Flask-MySQLdb
- MySQLClient
- Bootstrap 5.3

Installation:
1. Clone the repository.
2. Set up a virtual environment:
   python -m venv venv
3. Activate the virtual environment:
   - On Windows: venv\Scripts\activate
   - On macOS/Linux: source venv/bin/activate
4. Install the required packages:
   pip install -r requirements.txt
5. Set up the MySQL database using the `database.sql` file.
6. Update the MySQL configuration in `run.py` with your database credentials.

Running the App:
1. Run the Flask application:
   python run.py
2. Open your web browser and go to http://127.0.0.1:5000 to view the app. 