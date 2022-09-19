from json import dumps
from os import environ as env
from dotenv import load_dotenv
from flask import Flask, request
from flask_hmac import Hmac
from flask_hmac.exceptions import HmacException
from core.controller import Controller
from core.constants import SERVER_ERROR_CODE

load_dotenv()

app = Flask(__name__)
app.config['HMAC_KEY'] = env['HMAC_SECRET_KEY']
hmac = Hmac(app)

controller = Controller(env['DB_URI'])

@app.route('/api/expedientes', methods=['GET'])
def get_expedientes():
  return controller.get_expedientes(request.args)

@app.route('/api/documentos', methods=['GET'])
def get_documentos():
  # TODO: revisar estados de respuesta
  return controller.get_documentos(request.args)

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
