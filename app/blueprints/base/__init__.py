from flask import Blueprint

base = Blueprint(name='base', import_name=__name__, template_folder='templates', static_folder='static', static_url_path="/base", url_prefix='/')