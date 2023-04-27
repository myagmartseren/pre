from flask import Blueprint

services_bp = Blueprint('services', __name__, url_prefix='/services')

@services_bp.route('/')
def index():
    return 'This is the services index page.'
