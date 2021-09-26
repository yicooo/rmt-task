from flask_mongoengine import MongoEngine
from flask import Flask

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'main',
    'host': 'db',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)