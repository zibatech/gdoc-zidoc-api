from sqlalchemy.orm import sessionmaker, defer, deferred
from sqlalchemy.sql.functions import concat
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import InvalidRequestError
from .constants import EXCLUDED_FROM_DOCUMENTS

class Controller:

  session = None
  meta = None

  def __init__(self, uri):
    engine = create_engine(uri)
    DBSession = sessionmaker(bind=engine)
    self.meta = MetaData(engine)
    self.session = DBSession()
  
  def query(self, on, params, foreign_fields = []):
    try:
      table = Table(on, self.meta, autoload=True)          
      query = self.session.query(table, *foreign_fields).filter_by(**params)
      return query, table
    except InvalidRequestError as e:
      return {
        'error': True,
        'code': 'invalid_query',
        'message': str(e)
      }, None
  
  # TODO: generar la relacion de consultas
  def get_expedientes(self, params):
    trd_dependencia = Table('trd_dependencia', self.meta, autoload=True)
    trd_serie = Table('trd_serie', self.meta, autoload=True)
    trd_subserie = Table('trd_subserie', self.meta, autoload=True)
    usuarios = Table('usuarios', self.meta, autoload=True)

    query, table = self.query(
      'expedientes',
      params,
      [
        concat(
          trd_dependencia.c.Cod,
          ' - ',
          trd_dependencia.c.Nombre
        ).label('Dependencia'),
        concat(
          trd_serie.c.Cod,
          ' - ',
          trd_serie.c.Nombre
        ).label('Serie'),
        concat(
          trd_subserie.c.Cod,
          ' - ',
          trd_subserie.c.Nombre
        ).label('SubSerie'),
        usuarios.c.Nombre.label('Usuario')
      ]
    )
    if type(query) == dict and query.get('error'):
      return query

    result = query \
      .join(
        trd_dependencia, 
        trd_dependencia.c.id == table.c.Dependencia, 
        isouter=True
      ) \
      .join(
        trd_serie,
        trd_serie.c.id == table.c.Serie,
        isouter=True
      ) \
      .join(
        trd_subserie, 
        trd_subserie.c.id == table.c.SubSerie, 
        isouter=True
      ) \
      .join(
        usuarios, 
        usuarios.c.id == table.c.Usuario, 
        isouter=True
      )
    return { 'ok': True, 'data': [dict(row) for row in result] }

  def get_documentos(self, params):
    trd_tipodoc = Table('trd_tipodoc', self.meta, autoload=True)
    result, table = self.query(
      'documentos', 
      params,
      [
        concat(
          trd_tipodoc.c.Cod,
          ' - ',
          trd_tipodoc.c.Nombre
        ).label('TipoDoc')
      ]
    )
    if type(result) == dict and result.get('error'):
      return result
    
    data = result.join(
      trd_tipodoc,
      trd_tipodoc.c.Cod == table.c.TipoDoc,
      isouter=True
    )
    records = []
    for row in data:
      field = dict(row)
      for key in EXCLUDED_FROM_DOCUMENTS:
        del field[key]
      records.append(dict(field))
    return { 'ok': True, 'data': records }
