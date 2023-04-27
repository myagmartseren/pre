from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.views.users import *
from app.views.files import *