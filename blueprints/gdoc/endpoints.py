from flask import request
from . import gdoc
from core.controller import Controller
from os import environ as env

controller = Controller(env['GDOC_DB_URI'])

@gdoc.route('/expedientes', methods=['GET'])
def get_expedientes():
  return controller.get_expedientes(request.args)

@gdoc.route('/documentos', methods=['GET'])
def get_documentos():
  return controller.get_documentos(request.args)
