from flask import Blueprint

zidoc = Blueprint('zidoc', __name__)

from .endpoints.expedientes import *