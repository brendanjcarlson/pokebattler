from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

from .models import db, User
from .home.routes import home
from .auth.routes import auth
from .poke.routes import poke

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager()
login.init_app(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

login.login_view = 'auth.login_page'

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(poke, url_prefix='/poke')
