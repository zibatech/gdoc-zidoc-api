from sqlalchemy.orm import sessionmaker, defer, deferred
from sqlalchemy.sql.functions import concat
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import InvalidRequestError
from .constants import EXCLUDED_FROM_DOCUMENTS, SUCCESS_REQUEST, BAD_REQUEST

class Controller:

  session = None
  meta = None

  def __init__(self, uri):
    engine = create_engine(uri)
    DBSession = sessionmaker(bind=engine)
    self.meta = MetaData(engine)
    self.session = DBSession()
  
  def serialize(self, result):
    return [dict(row) for row in result]

  def response(self, data, status = SUCCESS_REQUEST):
    ok = status < 400
    _return = {'ok': ok}
    if ok:
      _return['data'] = data
    else:
      _return |= data
    return _return, status
  
  def query(self, name, params = {}, foreign_fields = []):
    try:
      table = Table(name, self.meta, autoload=True)
      params_copy = params.copy()
      aslike = []
      for param in params:
        if param.startswith('%'):
          value = params_copy.pop(param)
          field = param.replace('%', '')
          column = table.c[field]
          aslike.append(column.ilike(f'%{value}'))
      query = self.session.query(table, *foreign_fields) \
        .filter_by(**params_copy) \
        .filter(*aslike)
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
    return self.response(self.serialize(result))

  def get_documentos(self, params):
    params_dict = params.to_dict()
    if 'Asunto' in params_dict:
      params_dict['%Asunto'] = params_dict.pop('Asunto')
    result, table = self.query('documentos', params_dict)
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
    return self.response(records)

  def get_dependencias(self):
    query, table = self.query('trd_dependencia')
    rows = self.serialize(query)
    result = []
    for row in rows:
      result.append({
        'id': row['id'],
        'codigo': row['Cod'],
        'nombre': row['Nombre']
      })
    return self.response(result)

  def get_series(self, params):
    dependencia = params.get('dependencia')
    if not dependencia:
      return self.response(
        {'message': 'Dependencia no especificada.'},
        BAD_REQUEST
      )
    query, table = self.query(
      'trd_serie',
      { 'Dependencia': dependencia }
    )
    rows = self.serialize(query)
    result = []
    for row in rows:
      result.append({
        'id': row['id'],
        'codigo': row['Cod'],
        'nombre': row['Nombre']
      })
    return self.response(result)
  
  def get_subseries(self, params):
    clause = {}
    dependencia = params.get('dependencia')
    serie = params.get('serie')
    if dependencia:
      clause['Dependencia'] = dependencia
    if serie:
      clause['Serie'] = serie
    if len(clause) == 0:
      return self.response({
        'message': 'No se ha especificado dependencia y/o serie.'
      })
    query, _ = self.query('trd_subserie', clause)
    rows = self.serialize(query)
    result = []
    for row in rows:
      result.append({
        'id': row['id'],
        'codigo': row['Cod'],
        'nombre': row['Nombre']
      })
    return self.response(result)
  
  def get_tiposdoc(self, params):
    clause = {}
    dependencia = params.get('dependencia')
    serie = params.get('serie')
    subserie = params.get('subserie')
    if dependencia:
      clause['Dependencia'] = dependencia
    if serie:
      clause['Serie'] = serie
    if subserie:
      clause['Subserie'] = subserie
    if len(clause) == 0:
      return self.response({
        'message': 'No se ha especificado dependencia y/o serie y/o subserie.'
      })
    query, _ = self.query('trd_tipodoc', clause)
    rows = self.serialize(query)
    result = []
    for row in rows:
      result.append({ 'codigo': row['Cod'], 'nombre': row['Nombre'] })
    return self.response(result)
  
  def get_usuarios(self):
    query, _ = self.query('usuarios')
    rows = self.serialize(query)
    result = []
    for row in rows:
      result.append({ 'id': row['id'], 'nombre': row['Nombre'] })
    return self.response(result)
