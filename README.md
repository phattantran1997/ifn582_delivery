# Delivery Service Web App

This is a simple web application for a delivery service using Flask and MySQL.

## Requirements
blinker==1.9.0
Bootstrap-Flask==2.4.1
click==8.1.8
colorama==0.4.6
dnspython==2.7.0
dominate==2.9.1
email_validator==2.2.0
Flask==3.1.0
Flask-MySQLdb==2.0.0
Flask-WTF==1.2.2
greenlet==3.1.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.5
MarkupSafe==3.0.2
mysqlclient==2.2.7
numpy==2.2.2
typing_extensions==4.12.2
visitor==0.1.3
Werkzeug==3.1.3
WTForms==3.2.1


## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-team/flask-delivery-app.git
   cd flask-delivery-app
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   - Copy `example.env` to `.env`
   - Update the values in `.env` with your configuration
   - Required environment variables:
     - `MYSQL_HOST`: MySQL host (default: localhost)
     - `MYSQL_USER`: MySQL username
     - `MYSQL_PASSWORD`: MySQL password
     - `MYSQL_DB`: Database name
     - `FLASK_ENV`: Flask environment (development/production)
     - `FLASK_DEBUG`: Debug mode (1/0)

5. Set up the MySQL database using the `database.sql` file.

## Running the App

1. Run the Flask application:
   ```bash
   python run.py
   ```
2. Open your web browser and go to http://127.0.0.1:5000 to view the app.

## 🤝 Contribution Guide

### 1. Create a new branch for your work
```bash
git checkout -b feature/your-feature-name
```

### 2. Work on your feature
- Add code inside the appropriate module (api/, templates/, static/, etc.)
- Test your changes locally

### 3. Stage and commit your changes
```bash
git add .
git commit -m "Add: <short description of your feature>"
```

### 4. Push your branch to GitHub
```bash
git push origin feature/your-feature-name
```

### 5. Open a Pull Request
- Go to GitHub and open a pull request to merge your branch into main
- Request a review from the team lead

### 6. Sync regularly
Before starting new work:
```bash
git checkout main
git pull origin main
``` 