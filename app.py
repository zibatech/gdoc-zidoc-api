from flask import Flask
from blueprints.zidoc import zidoc

app = Flask(__name__)

app.register_blueprint(zidoc, url_prefix='/zidoc')
