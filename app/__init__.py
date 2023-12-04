from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from app.models import db, User

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager()
login.init_app(app)
login.login_view = 'auth.login'

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from app.blueprints.base import base
app.register_blueprint(base)

from app.blueprints.site import site
app.register_blueprint(site)