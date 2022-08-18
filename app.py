from flask import Flask
from dotenv import load_dotenv
from blueprints.zidoc import zidoc

load_dotenv()

app = Flask(__name__)

app.register_blueprint(zidoc, url_prefix='/zidoc')
