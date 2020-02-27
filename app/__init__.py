import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

# Importing the configuration settings from the config class file
app.config.from_object(Config)
# adding bootstrap to the app
bootstrap = Bootstrap(app)
moment = Moment(app)
# Setting up the DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Login state object
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors # this must be located after app configurations


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/flask-blog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask-Blog startup')
