from flask import Blueprint

site = Blueprint(name='site', import_name=__name__, template_folder='templates', static_folder='static', url_prefix='/', static_url_path='/site')

from app.blueprints.site import routes

_ = routes