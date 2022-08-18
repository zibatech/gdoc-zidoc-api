
# tiene que heredar de alguna base de datos

class ExpedientesController:

  def get_clause(self, params):
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

  def get(self, params):
    clause, values = self.get_clause(params)
    statement = f'SELECT * FROM expedientes WHERE {clause}'
    query = self.cursor.execute(statement, values)
    rows = self.cursor.fetchall()
    return rows
