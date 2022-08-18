from flask import request
from . import gdoc
from shared.controllers import Controller
from shared.databases import GDoc

class GDocController(Controller, GDoc):
  pass

controller = GDocController()

@gdoc.route('/expedientes', methods=['GET'])
def get_expedientes():
  return controller.get_expedientes(request.args)

@gdoc.route('/documentos', methods=['GET'])
def get_documentos():
  return controller.get_documentos(request.args)
