from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import concat
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import InvalidRequestError

class Controller:

  session = None
  meta = None

  def __init__(self, uri):
    engine = create_engine(uri)
    DBSession = sessionmaker(bind=engine)
    self.meta = MetaData(engine)
    self.session = DBSession()
  
  def query(self, table_name, clause, f_keys = []):
    try:
      table = Table(table_name, self.meta, autoload=True)
      result = self.session.query(table, *f_keys).filter_by(**clause)
      return result, table
    except InvalidRequestError as e:
      return { 'error': True, 'code': 'invalid_query', 'message': str(e) }
  
  def get_expedientes(self, params):
    trd_dependencias = Table('trd_dependencias', self.meta, autoload=True)
    trd_series = Table('trd_series', self.meta, autoload=True)
    trd_subseries = Table('trd_subseries', self.meta, autoload=True)
    soportes = Table('soportes', self.meta, autoload=True)
    unidades_conservacion = Table(
      'unidades_conservacion',
      self.meta,
      autoload=True
    )
    result, table = self.query(
      'expedientes',
      params,
      [
        concat(
          trd_dependencias.c.codigo,
          ' - ',
          trd_dependencias.c.nombre
        ).label('dependencia'),
        concat(trd_series.c.codigo, ' - ', trd_series.c.nombre).label('serie'),
        concat(
          trd_subseries.c.codigo,
          ' - ',
          trd_subseries.c.nombre
        ).label('subserie'),
        soportes.c.nombre.label('soporte'),
        unidades_conservacion.c.nombre.label('unidad_conservacion')
      ]
    )
    if type(result) == dict and result.get('error'):
      return result      

    data = result \
      .join(
        trd_dependencias, 
        trd_dependencias.c.id == table.c.dependencia, 
        isouter=True
      ) \
      .join(
        trd_series,
        trd_series.c.id == table.c.serie,
        isouter=True
      ) \
      .join(
        trd_subseries, 
        trd_subseries.c.id == table.c.subserie, 
        isouter=True
      ) \
      .join(
        soportes,
        soportes.c.id == table.c.soporte,
        isouter=True
      ) \
      .join(
        unidades_conservacion,
        unidades_conservacion.c.id == table.c.unidad_conservacion,
        isouter=True
      )
    return { 'ok': True, 'data': [dict(row) for row in data] }

  def get_documentos(self, params):
    trd_tiposdoc = Table('trd_tiposdoc', self.meta, autoload=True)
    result, table = self.query(
      'documentos',
      params,
      [
        concat(
          trd_tiposdoc.c.codigo,
          ' - ',
          trd_tiposdoc.c.nombre
        ).label('tipo_documental')
      ]
    )
    if type(result) == dict and result.get('error'):
      return result
    
    data = result.join(
      trd_tiposdoc,
      trd_tiposdoc.c.id == table.c.tipo_documental,
      isouter=True
    )
    return { 'ok': True, 'data': [dict(row) for row in data] }