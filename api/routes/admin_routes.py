from flask import Blueprint, render_template, request, redirect, url_for
from api.routes.base_routes import BaseRoute
from api.services.product_service import ProductService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_route = BaseRoute(ProductService)

@admin_bp.route('/', methods=['GET'])
def home():
    products = admin_route.service.get_all_products()
    return render_template('admin.html', products=products)

@admin_bp.route('/products/add', methods=['GET'])
def add_product_page():
    categories = admin_route.service.get_categories()
    if request.args.get('id'):
        product = admin_route.service.get_product_by_id(request.args.get('id'))
    else:
        product = None
    return render_template('admin_product.html', categories=categories, product=product)

@admin_bp.route('/products/add', methods=['POST'])
def add_new_product():
    data = request.form
    admin_route.service.create_product(data)
    return redirect(url_for('admin.home'))

@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
def delete_product(id):
    admin_route.service.delete_product(id)
    return redirect(url_for('admin.home'))

@admin_bp.route('/products/<int:id>/update', methods=['POST'])
def update_product(id):
    data = request.form
    admin_route.service.update_product(id, data)
    return redirect(url_for('admin.home'))

@admin_bp.route('/category/add', methods=['POST'])
def add_new_category():
    try:
        data = request.form
        category = admin_route.service.create_category(data)
        return jsonify({'status': 'success', 'message': 'Category added successfully', 'data': category}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

