import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object): # Config class for setting environment variables
    # For protection from CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something-special'
    
    # For connection to the db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For email notifications of errors if I want to set that up
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['jake@graham4.org']