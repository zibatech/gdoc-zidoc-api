from json import dumps
from dotenv import load_dotenv
from flask import Flask
from blueprints.zidoc import zidoc
from blueprints.gdoc import gdoc
from core.constants import SERVER_ERROR_CODE

load_dotenv()

app = Flask(__name__)

app.register_blueprint(zidoc, url_prefix='/zidoc')
app.register_blueprint(gdoc, url_prefix='/gdoc')

@app.errorhandler(SERVER_ERROR_CODE)
def handle_exception(e):
  response = e.get_response()
  response.data = dumps({
    'code': e.code,
    'type': e.name,
    'description': e.description
  })
  response.content_type = 'application/json'
  return response
