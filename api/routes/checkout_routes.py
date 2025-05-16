from flask import Blueprint, render_template

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout', methods=['GET'])
def checkout_page():
    return render_template('checkout.html')


