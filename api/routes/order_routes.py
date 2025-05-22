from flask import Blueprint, render_template, session
from utils.decorators import user_required
from api.services.order_service import OrderService
from api.routes.base_routes import BaseRoute

order_bp = Blueprint('order', __name__)
order_service = BaseRoute(OrderService)

@order_bp.route('/orders/history')
@user_required
def history():
    user_id = session['user_id']
    orders = order_service.service.get_orders_by_user_id(user_id)
    return render_template('order_history.html', orders=orders)
