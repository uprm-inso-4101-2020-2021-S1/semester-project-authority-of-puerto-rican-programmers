from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fe40e37e9db438bbf8710933764c98bb'

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
#  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cande2nba@localhost:8000/Cande'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ybvcezhsbtthew:c25e2e381493ce7f44698d77ca1f30ab3828f97820045c2102e9868d7aed22c8@ec2-18-210-90-1.compute-1.amazonaws.com/d1j12hfu81fusv'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from my_app import routes
