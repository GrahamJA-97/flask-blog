from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Importing the configuration settings from the config class file
app.config.from_object(Config)
# Setting up the DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Login state object
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
