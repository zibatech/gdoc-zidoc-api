from json import dumps
from os import environ as env

from dotenv import load_dotenv
from flask import Flask, request
from flask_hmac import Hmac
from flask_hmac.exceptions import HmacException

from core.constants import SERVER_ERROR_CODE
from core import controllers

load_dotenv()

app = Flask(__name__)
app.config['HMAC_KEY'] = env['HMAC_SECRET_KEY']
hmac = Hmac(app)


@app.route('/api/dependencias', methods=['GET'])
def get_dependencias():
    controller = controllers.DependenciasController()
    return controller.get()


@app.route('/api/series', methods=['GET'])
def get_series():
    controller = controllers.SeriesController()
    return controller.get(request.args)


@app.route('/api/subseries', methods=['GET'])
def get_subseries():
    controller = controllers.SubseriesController()
    return controller.get(request.args)


@app.route('/api/tipos-documentales', methods=['GET'])
def get_tiposdoc():
    controller = controllers.TiposDocController()
    return controller.get(request.args)


@app.route('/api/expedientes', methods=['GET'])
def get_expedientes():
    controller = controllers.ExpedientesController()
    return controller.get(request.args)


@app.route('/api/documentos', methods=['GET'])
def get_documentos():
    controller = controllers.DocumentosController()
    return controller.get(request.args)


@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    controller = controllers.UsuariosController()
    return controller.get()


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
