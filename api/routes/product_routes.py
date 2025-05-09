from flask import Blueprint, jsonify, request
from api.services.product_service import ProductService
from api.routes.base_routes import BaseRoute

product_bp = Blueprint('product', __name__, url_prefix='/api/products')
product_route = BaseRoute(ProductService)

@product_bp.route('/', methods=['GET'])
def get_products():
    try:
        products = product_route.service.get_all_products()
        return jsonify({'status': 'success', 'data': products}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = product_route.service.get_product_by_id(id)
        return jsonify({'status': 'success', 'data': product}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "Product not found" else 500

@product_bp.route('/', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        product = product_route.service.create_product(data)
        return jsonify({'status': 'success', 'message': 'Product created successfully', 'data': product}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400 if "Missing required field" in str(e) else 500

@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()
        product = product_route.service.update_product(id, data)
        return jsonify({'status': 'success', 'message': 'Product updated successfully', 'data': product}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "Product not found" else 400 if str(e) == "No fields to update" else 500

@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product_route.service.delete_product(id)
        return jsonify({'status': 'success', 'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404 if str(e) == "Product not found" else 500
