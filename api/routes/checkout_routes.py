import decimal

from utils.decorators import user_required
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from api.routes.base_routes import BaseRoute
from api.services.order_service import OrderService
from api.services.cart_service import CartService
from api.forms.checkout_form import CheckoutForm

checkout_bp = Blueprint('checkout', __name__)
checkout_service = BaseRoute(OrderService)
cart_service = BaseRoute(CartService)

@checkout_bp.route('/carts/<int:cart_id>/checkout', methods=['GET', 'POST'])
@user_required
def index(cart_id):
    try:
        selected_delivery_method_id = request.form['delivery_method_id'] if 'delivery_method_id' in request.form else 2
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
    except Exception as e:
        return render_template('error.html', error=str(e))

@checkout_bp.route('/carts/<int:cart_id>/checkout/place_order', methods=['POST'])
@user_required
def place_order(cart_id):
    form = CheckoutForm(request.form)
    if not form.validate_on_submit():
        form_errors = form.errors
        flash(', '.join(form_errors.values()), 'error')
        return redirect(url_for('checkout.index', cart_id=cart_id))

    try:
        user_id = session['user_id']
        selected_delivery_method_id = request.args['selected_delivery_method_id']
        selected_delivery_method = checkout_service.service.get_all_shipping_methods()[int(selected_delivery_method_id) - 1]
        _, _, total_amount = _calculate_total(cart_id, selected_delivery_method)
        checkout_service.service.create_order(
            recipient_name=' '.join([form.first_name.data, form.last_name.data]),
            phone=form.phone.data,
            address=', '.join([form.address.data,form.city.data,form.state.data,str(form.zip_code.data)]),
            delivery_method_id=selected_delivery_method_id,
            user_id=user_id,
            cart_id=cart_id,
            total_amount=total_amount
        )
        flash('Order placed successfully', 'success')
        return redirect(url_for('order.history'))
    except Exception as e:
        return render_template('error.html', error=str(e))

def _calculate_total(cart_id: int, delivery_method):
    subtotal = cart_service.service.get_cart_subtotal(cart_id)
    # GST => 10%
    tax = subtotal * decimal.Decimal('0.1')
    total = subtotal + tax + delivery_method.fee
    return subtotal, tax, total
    
    
    


