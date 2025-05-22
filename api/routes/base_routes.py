from flask import Blueprint, render_template, request
from utils.mysql_init import MySQLManager
from api.services.product_service import ProductService

class BaseRoute:
    def __init__(self, service_class):
        self.service_class = service_class
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.service_class()
        return self._service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    product_service = ProductService()
    category = request.args.get('category')
    search = request.args.get('search')
    products = product_service.get_all_products(category=category, search=search)
    categories = product_service.get_categories()
    return render_template('homepage.html', products=products, categories=categories)

@main_bp.route('/error')
def error():
    return render_template('error.html', error="Something went wrong")

@main_bp.route('/500')
def internal_server_error():
    raise Exception("Internal Server Error")