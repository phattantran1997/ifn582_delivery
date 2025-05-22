import os
from utils.decorators import admin_required
from flask import Blueprint, render_template, request, redirect, url_for
from api.routes.base_routes import BaseRoute
from api.services.product_service import ProductService
from api.services.order_service import OrderService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_route = BaseRoute(ProductService)
order_route = BaseRoute(OrderService)

@admin_bp.route('/', methods=['GET'])
@admin_required
def home():
    products = admin_route.service.get_all_products()
    return render_template('admin.html', products=products, section='products')

@admin_bp.route('/products/add', methods=['GET'])
@admin_required
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
    # handle image upload
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        file.save(os.path.join(os.path.curdir, 'static/images/products', file.filename))

    admin_route.service.create_product({
        'name': data['name'],
        'price': data['price'],
        'category_id': data['category_id'],
        'image': os.path.join('images/products', file.filename),
        'description': data['description']
    })
    return redirect(url_for('admin.home'))

@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
def delete_product(id):
    admin_route.service.delete_product(id)
    return redirect(url_for('admin.home'))

@admin_bp.route('/products/<int:id>/update', methods=['POST'])
def update_product(id):
    data = request.form
    updated_fields = {
        'name': data['name'],
        'price': data['price'],
        'category_id': data['category_id'],
        'description': data['description']
    }

    # handle image upload
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        file.save(os.path.join(os.path.curdir, 'static/images/products', file.filename))
        updated_fields['image'] = os.path.join('images/products', file.filename)

    admin_route.service.update_product(id, updated_fields)
    return redirect(url_for('admin.home'))

@admin_bp.route('/category/add', methods=['GET'])
@admin_required
def add_category_page():
    categories = admin_route.service.get_categories()
    if request.args.get('id'):
        category = admin_route.service.get_category_by_id(request.args.get('id'))
    else:
        category = None
    return render_template('admin_category.html', categories=categories, category=category)

@admin_bp.route('/category/add', methods=['POST'])
def add_new_category():
    try:
        name = request.form['name']
        admin_route.service.create_category(name)
        return redirect(url_for('admin.categories'))
    except Exception as e:
        return render_template('500.html')

@admin_bp.route('/category/<int:id>/update', methods=['POST'])
def update_category(id):
    try:
        name = request.form['name']
        admin_route.service.update_category(id, name)
        return redirect(url_for('admin.categories'))
    except Exception as e:
        return render_template('500.html')
    

@admin_bp.route('/categories', methods=['GET'])
@admin_required
def categories():
    categories = admin_route.service.get_categories()
    return render_template('category.html', categories=categories, section='categories')

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def orders():
    orders = order_route.service.get_orders_by_user_id()
    return render_template('admin.html', orders=orders, section='orders')
    
