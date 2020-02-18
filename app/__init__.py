from flask import Flask
from config import Config

app = Flask(__name__)

# Importing the configuration settings from the config class file
app.config.from_object(Config) #


from app import routes
