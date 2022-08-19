class Controller: # heredar de una base de datos

  def get_clause(self, params):
    if len(params) == 0:
      return 1, ()
    params_dict = dict(params)
    clause = ''
    values = []
    i = 1
    for param in params_dict:
      value = params_dict[param]
      field_clause = f'{param} = %s'
      if i < len(params_dict):
        field_clause += ' AND '
      clause += field_clause
      values.append(value)
      i += 1
    values = tuple(values)
    return clause, values

  def get_expedientes(self, params):
    clause, values = self.get_clause(params)
    statement = f"""
      SELECT *, CONCAT('/documentos?Expediente=', expedientes.id) AS documentos
      FROM expedientes WHERE {clause}
    """
    self.cursor.execute(statement, values)
    return self.cursor.fetchall()
  
  def get_documentos(self, params):
    clause, values = self.get_clause(params)
    statement = f'SELECT * FROM documentos WHERE {clause}'
    self.cursor.execute(statement, values)
    return self.cursor.fetchall()
