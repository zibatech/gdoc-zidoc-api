from core.controller import Controller


class SubseriesController(Controller):

    def get(self, params=None):
        if params is None:
            params = {}
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
