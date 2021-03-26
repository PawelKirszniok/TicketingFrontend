from flask import Flask
from ticketingfrontend.cache import CacheService
from configparser import ConfigParser
from flask_login import LoginManager

config_object = ConfigParser()
config_object.read('TicketingBackground/TicketingFrontend/ticketingfrontend/config.ini')
keys = config_object['KEYS']
app = Flask(__name__)
app.config['SECRET_KEY'] = keys['local_key']
cache_service = CacheService()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from ticketingfrontend.data import DataService
database_service = DataService()

from ticketingfrontend import routes