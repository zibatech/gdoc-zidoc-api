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
  
  def query(self, name, params = {}, foreign_fields = []):
    try:
      table = Table(name, self.meta, autoload=True)          
      query = self.session.query(table, *foreign_fields).filter_by(**params)
      return query, table
    except InvalidRequestError as e:
      return {
        'error': True,
        'code': 'invalid_query',
        'message': str(e)
      }, None

  def get_expedientes(self, params):
    trd_dependencia = Table('trd_dependencia', self.meta, autoload=True)
    trd_serie = Table('trd_serie', self.meta, autoload=True)
    trd_subserie = Table('trd_subserie', self.meta, autoload=True)
    usuarios = Table('usuarios', self.meta, autoload=True)

    pasdict = params.to_dict()
    dependencia = pasdict.get('Dependencia', None)
    if dependencia:
      dependencia_id, _ = self.query(
        'trd_dependencia',
        { 'Cod': dependencia }
      )
      pasdict['Dependencia'] = dict(dependencia_id.first()).get('id')
    
    serie = pasdict.get('Serie', None)
    if serie:
      clause = { 'Cod': serie }
      if dependencia:
        clause['Dependencia'] = dependencia
      serie_id, _ = self.query('trd_serie', clause)
      pasdict['Serie'] = dict(serie_id.first()).get('id')
    
    subserie = pasdict.get('SubSerie', None)
    if subserie:
      clause = { 'Cod': subserie }
      if serie:
        clause['Serie'] = serie
      if dependencia:
        clause['Dependencia'] = dependencia
      subserie_id, _ = self.query('trd_subserie', clause)
      pasdict['SubSerie'] = dict(subserie_id.first()).get('id')
    
    query, table = self.query(
      'expedientes',
      pasdict,
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
    result, table = self.query('documentos', params)
    if type(result) == dict and result.get('error'):
      return result
    records = []
    for row in result:
      field = dict(row)
      for key in EXCLUDED_FROM_DOCUMENTS:
        del field[key]
      tipodoc = field.get('TipoDoc')
      if tipodoc != "9":
        tipodoc_res, _ = self.query('trd_tipodoc', { 'Cod': tipodoc })
        tipodoc_row = dict(tipodoc_res.first())
        field['TipoDoc'] = f"{tipodoc_row['Cod']} - {tipodoc_row['Nombre']}"      
      records.append(dict(field))
    return { 'ok': True, 'data': records }
