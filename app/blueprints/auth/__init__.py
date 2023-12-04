from flask import Blueprint

auth = Blueprint(name='auth', import_name=__name__, template_folder="templates", static_folder="static", static_url_path="/auth", url_prefix="/")

from app.blueprints.auth import routes, forms

_ = (routes, forms)