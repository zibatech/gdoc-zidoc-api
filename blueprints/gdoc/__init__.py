from flask import Blueprint

gdoc = Blueprint('gdoc', __name__)

from .endpoints import *