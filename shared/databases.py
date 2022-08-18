from mysql.connector import connect
from os import environ as env

class Database:

  connection = None
  cursor = None

  def __init__(self, config):
    self.connection = connect(**config)
    self.cursor = self.connection.cursor(dictionary=True)
  
class ZiDoc(Database):

  def __init__(self):
    super().__init__({
      'host': env.get('ZIDOC_DB_HOST'),
      'database': env.get('ZIDOC_DB_NAME'),
      'user': env.get('ZIDOC_DB_USER'),
      'password': env.get('ZIDOC_DB_PASSWORD')
    })

class GDoc(Database):

  def __init__(self):
    super().__init__({
      'host': env.get('GDOC_DB_HOST'),
      'database': env.get('GDOC_DB_NAME'),
      'user': env.get('GDOC_DB_USER'),
      'password': env.get('GDOC_DB_PASSWORD')
    })