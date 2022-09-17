from json import dumps
from os import environ as env
from dotenv import load_dotenv
from flask import Flask, request
from flask_hmac import Hmac
from flask_hmac.exceptions import HmacException
from blueprints.gdoc import gdoc
from blueprints.zidoc import zidoc
from core.constants import SERVER_ERROR_CODE

load_dotenv()

app = Flask(__name__)
app.config['HMAC_KEY'] = env['HMAC_SECRET_KEY']
hmac = Hmac(app)

app.register_blueprint(zidoc, url_prefix='/zidoc')
app.register_blueprint(gdoc, url_prefix='/gdoc')

@app.before_request
def hmac_validation():
  try:
    hmac.validate_signature(request)
  except HmacException:
    return hmac.abort()

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
