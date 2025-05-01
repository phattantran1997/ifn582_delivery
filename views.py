from flask import Blueprint, render_template

# Create a blueprint for the main routes
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    # Render the landing page
    return render_template('index.html') 