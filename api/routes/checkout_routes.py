from flask import Blueprint, render_template, request
from api.routes.base_routes import BaseRoute
from api.services.order_service import OrderService
from api.services.cart_service import CartService

checkout_bp = Blueprint('checkout', __name__)
checkout_service = BaseRoute(OrderService)
cart_service = BaseRoute(CartService)

@checkout_bp.route('/carts/<int:cart_id>/checkout', methods=['GET'])
def index(cart_id):
    shipping_methods = checkout_service.service.get_all_shipping_methods()
    cart = cart_service.service.get_cart_by_id(cart_id)
    selected_delivery_method = shipping_methods[2]
    return render_template(
        'checkout.html',
        cart=cart,
        delivery_options=shipping_methods,
        selected_delivery_method=selected_delivery_method
    )

@checkout_bp.route('/carts/<int:cart_id>/checkout/update_delivery', methods=['POST'])
def update_delivery(cart_id):
    selected_delivery_method_id = request.form['delivery_method_id']
    cart = cart_service.service.get_cart_by_id(cart_id)
    shipping_methods = checkout_service.service.get_all_shipping_methods()
    selected_delivery_method = shipping_methods[int(selected_delivery_method_id) - 1]
    return render_template(
        'checkout.html',
        cart=cart,
        delivery_options=shipping_methods,
        selected_delivery_method=selected_delivery_method
    )
    
    


