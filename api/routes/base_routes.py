from flask import Blueprint, render_template
from utils.mysql_init import MySQLManager

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
    return render_template('index.html')

@main_bp.route('/bedroom')
def bedroom():
    return render_template('bedroom.html')

@main_bp.route('/dining')
def dining():
    return render_template('dining.html')

@main_bp.route('/living-room')
def living_room():
    return render_template('living-room.html')

@main_bp.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@main_bp.route('/cleaning')
def cleaning():
    return render_template('cleaning.html')

@main_bp.route('/bathroom')
def bathroom():
    return render_template('bathroom.html')

@main_bp.route('/track-order')
def track_order():
    return render_template('tracking.html')

@main_bp.route('/cart')
def cart():
    return render_template('cart.html')

@main_bp.route('/product/<category>/<product>')
def product_details(category, product):
    return render_template('product_details.html', category=category, product=product)