from flask import Blueprint

auth = Blueprint(name='auth', import_name=__name__, template_folder="auth_templates", static_folder="auth_static")

from app.blueprints.auth import routes, forms

_ = (routes, forms)