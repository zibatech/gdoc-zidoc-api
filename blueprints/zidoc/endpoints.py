from flask import request
from . import zidoc
from core.controller import Controller
from os import environ as env

controller = Controller(env['ZIDOC_DB_URI'])

@zidoc.route('/expedientes', methods=['GET'])
def get_expedientes():
  return controller.get_expedientes(request.args)

@zidoc.route('/documentos', methods=['GET'])
def get_documentos():
  return controller.get_documentos(request.args)
