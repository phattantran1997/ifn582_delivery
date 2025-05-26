import decimal

from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from utils.decorators import user_required
from api.services.cart_service import CartService
from api.routes.base_routes import BaseRoute
from api.forms.cart_form import AddToCartForm

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_route = BaseRoute(CartService)

@cart_bp.route('/', methods=['GET'])
@user_required
def cart_page():
    # get user id from session
    user_id = session.get('user_id')
    try:
        cart = cart_route.service.get_cart_by_user_id(user_id)
        if cart is None:
            return render_template('cart.html', cart=cart, subtotal=0, tax=0, total=0)

        subtotal, tax, total = _calculate_total(cart.id)
        return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)
    except Exception as e:
        return render_template('error.html', error=str(e))

@cart_bp.route('/<int:cart_id>/cart_items/<int:cart_item_id>/minus', methods=['POST'])
@user_required 
def minus_quantity(cart_id, cart_item_id):
    try:
        if not _is_self_cart(cart_id):
            return render_template('error.html', error='You are not authorized to update this cart item')
        # check if quantity is larger than 0
        quantity = cart_route.service.get_cart_item_quantity(cart_item_id)
        cart = cart_route.service.get_cart_by_id(cart_id)

        if quantity <= 1:
            subtotal, tax, total = _calculate_total(cart.id)
            return render_template('cart.html', cart=cart, subtotal=subtotal, tax=tax, total=total)

        cart_route.service.update_cart_item_quantity(cart_item_id, -1)
        return redirect(url_for('cart.cart_page'))
    except Exception as e:
        return render_template('error.html', error=str(e))

@cart_bp.route('/<int:cart_id>/cart_items/<int:cart_item_id>/add', methods=['POST'])
@user_required
def plus_quantity(cart_id, cart_item_id):
    try:
        if not _is_self_cart(cart_id):
            return render_template('error.html', error='You are not authorized to update this cart item')
        cart_route.service.update_cart_item_quantity(cart_item_id, 1)
        return redirect(url_for('cart.cart_page'))
    except Exception as e:
        return render_template('error.html', error=str(e))

@cart_bp.route('/<int:cart_id>/cart_items/<int:cart_item_id>/delete', methods=['POST'])
@user_required
def delete_cart_item(cart_id, cart_item_id):
    try:
        if not _is_self_cart(cart_id):
            return render_template('error.html', error='You are not authorized to delete this cart item')
        cart_route.service.delete_cart_item(cart_item_id)
        return redirect(url_for('cart.cart_page'))
    except Exception as e:
        return render_template('error.html', error=str(e))

@cart_bp.route('/add_to_cart', methods=['POST'])
@user_required
def add_to_cart():
    product_id = request.args.get('product_id')
    form = AddToCartForm(request.form)
    try:
        user_id = session.get('user_id')
        if user_id is None:
            flash('Please log in first', 'error')
            return redirect(url_for('auth.login_page'))

        if form.validate_on_submit():
            cart = cart_route.service.get_cart_by_user_id(user_id)
            print(cart)
            if cart is None:
                cart = cart_route.service.create_cart(user_id)

            cart_item = cart_route.service.get_cart_item_by_product_id(cart.id, product_id)
            # if cart item exists, just update quantity
            selected_qty = int(form.quantity.data)

            if cart_item is not None:
                cart_route.service.update_cart_item_quantity(cart_item.id, selected_qty)
            else:
                cart_route.service.add_to_cart(cart.id, product_id, selected_qty)

            flash('Product added to cart', 'success')

        return redirect(url_for('cart.cart_page'))

    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('product.get_product', id=product_id))


def _calculate_total(cart_id: int):
    subtotal = cart_route.service.get_cart_subtotal(cart_id)
    # GST => 10%
    tax = subtotal * decimal.Decimal('0.1')
    total = subtotal + tax
    return subtotal, tax, total

def _is_self_cart(cart_id: int):
    user_id = session.get('user_id')
    cart = cart_route.service.get_cart_by_id(cart_id)
    return cart.user_id == user_id
    
    