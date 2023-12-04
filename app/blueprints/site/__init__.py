from flask import Blueprint

site = Blueprint('site', __name__, template_folder='templates', static_folder='static', url_prefix='/')

from app.blueprints.site import routes

_ = routes