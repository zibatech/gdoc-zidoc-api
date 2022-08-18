from flask import request
from . import zidoc
from shared.controllers import Controller
from shared.databases import ZiDoc

class ZiDocController(Controller, ZiDoc):
  pass

controller = ZiDocController()

@zidoc.route('/expedientes', methods=['GET'])
def get_expedientes():
  return controller.get_expedientes(request.args)

@zidoc.route('/documentos', methods=['GET'])
def get_documentos():
  return controller.get_documentos(request.args)
