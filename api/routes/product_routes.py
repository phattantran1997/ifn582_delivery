from flask import Blueprint, jsonify, request, render_template
from api.services.product_service import ProductService
from api.routes.base_routes import BaseRoute
from api.forms.cart_form import AddToCartForm

product_bp = Blueprint('product', __name__, url_prefix='/products')
product_route = BaseRoute(ProductService)


@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    try:
        form = AddToCartForm()
        product = product_route.service.get_product_by_id(id)
        return render_template('product_details.html', product=product, form=form)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "Product not found" else 500
