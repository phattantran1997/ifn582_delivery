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
    try:
        cart = cart_route.service.get_cart_by_user_id(user_id)
        subtotal, tax, total = _calculate_total(cart.id)
        return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cart_bp.route('/<int:cart_id>/cart_items/<int:cart_item_id>/minus', methods=['POST'])
def minus_quantity(cart_id, cart_item_id):
    try:
        # check if quantity is larger than 0
        quantity = cart_route.service.get_cart_item_quantity(cart_item_id)
        cart = cart_route.service.get_cart_by_id(cart_id)

        if quantity <= 1:
            subtotal, tax, total = _calculate_total(cart.id)
            return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)

        cart_route.service.update_cart_item_quantity(cart_item_id, -1)
        cart = cart_route.service.get_cart_by_id(cart_id)
        subtotal, tax, total = _calculate_total(cart.id)
        return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cart_bp.route('/<int:cart_id>/cart_items/<int:cart_item_id>/add', methods=['POST'])
def plus_quantity(cart_id, cart_item_id):
    try:
        cart_route.service.update_cart_item_quantity(cart_item_id, 1)
        cart = cart_route.service.get_cart_by_id(cart_id)
        subtotal, tax, total = _calculate_total(cart.id)
        return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@cart_bp.route('/<int:cart_id>/cart_items/<int:cart_item_id>/delete', methods=['POST'])
def delete_cart_item(cart_id, cart_item_id):
    try:
        cart_route.service.delete_cart_item(cart_item_id)
        cart = cart_route.service.get_cart_by_id(cart_id)
        subtotal, tax, total = _calculate_total(cart.id)
        return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def _calculate_total(cart_id: int):
    subtotal = cart_route.service.get_cart_subtotal(cart_id)
    # GST => 10%
    tax = subtotal * decimal.Decimal('0.1')
    total = subtotal + tax
    return subtotal, tax, total
    