import decimal

from flask import Blueprint, jsonify, session, render_template
from api.services.cart_service import CartService
from api.routes.base_routes import BaseRoute

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_route = BaseRoute(CartService)

@cart_bp.route('/', methods=['GET'])
def cart_page():
    # get user id from session
    user_id = session.get('user_id')
    print("user_id: ", user_id)
    try:
        cart = cart_route.service.get_cart_by_user_id(user_id)
        subtotal = cart_route.service.get_cart_subtotal(cart.id)
        shipping = 0
        # GST => 10%
        tax = subtotal * decimal.Decimal('0.1')
        total = subtotal + shipping + tax
        return render_template('cart.html', cart_items=cart.cart_items, subtotal=subtotal, shipping=shipping, tax=tax, total=total)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
