from flask import Blueprint

base = Blueprint('base', __name__, template_folder='templates', static_folder='static', url_prefix='/')