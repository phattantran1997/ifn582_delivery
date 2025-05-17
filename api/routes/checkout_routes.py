import decimal
from flask import Blueprint, render_template, request, session
from api.routes.base_routes import BaseRoute
from api.services.order_service import OrderService
from api.services.cart_service import CartService
from api.forms.checkout_form import CheckoutForm

checkout_bp = Blueprint('checkout', __name__)
checkout_service = BaseRoute(OrderService)
cart_service = BaseRoute(CartService)

@checkout_bp.route('/carts/<int:cart_id>/checkout', methods=['GET', 'POST'])
def index(cart_id):
    selected_delivery_method_id = request.form['delivery_method_id'] if 'delivery_method_id' in request.form else 2
    print(selected_delivery_method_id)
    shipping_methods = checkout_service.service.get_all_shipping_methods()
    cart = cart_service.service.get_cart_by_id(cart_id)
    selected_delivery_method = shipping_methods[int(selected_delivery_method_id) - 1]
    form = CheckoutForm()
    subtotal, tax, total = _calculate_total(cart_id, selected_delivery_method)
    return render_template(
        'checkout.html',
        cart=cart,
        delivery_options=shipping_methods,
        form=form,
        selected_delivery_method=selected_delivery_method,
        subtotal=subtotal,
        tax=tax,
        total=total
    )

@checkout_bp.route('/carts/<int:cart_id>/checkout/place_order', methods=['POST'])
def place_order(cart_id):
    user_id = session['user_id']
    selected_delivery_method_id = request.args['selected_delivery_method_id']
    selected_delivery_method = checkout_service.service.get_all_shipping_methods()[int(selected_delivery_method_id) - 1]
    _, _, total_amount = _calculate_total(cart_id, selected_delivery_method)
    order = checkout_service.service.create_order(
        recipient_name=request.form['first_name'] + ' ' + request.form['last_name'],
        phone=request.form['phone'],
        address=','.join([request.form['address'],request.form['city'],request.form['state'],request.form['zip_code']]),
        delivery_method_id=selected_delivery_method_id,
        user_id=user_id,
        cart_id=cart_id,
        total_amount=total_amount
    )
    return render_template('tracking.html')

def _calculate_total(cart_id: int, delivery_method):
    subtotal = cart_service.service.get_cart_subtotal(cart_id)
    # GST => 10%
    tax = subtotal * decimal.Decimal('0.1')
    total = subtotal + tax + delivery_method.fee
    return subtotal, tax, total
    
    
    


