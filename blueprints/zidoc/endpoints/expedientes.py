from flask import request
from .. import zidoc
from shared.controllers.expedientes import ExpedientesController
from shared.services.database import ZiDoc

class Controller(ExpedientesController, ZiDoc):
  pass

controller = Controller()

@zidoc.route('/expedientes', methods=['GET'])
def get_expedientes():
  params = request.args
  result = controller.get(request.args)
  return result
  