from core.controller import Controller


class TiposDocController(Controller):

    def get(self, params=None):
        if params is None:
            params = {}
        if len(params) == 0:
            return self.response({
                'message': 'No se ha especificado dependencia y/o serie y/o '
                           'subserie. '
            })
        dependencia = params.get('dependencia')
        serie = params.get('serie')
        subserie = params.get('subserie')
        if dependencia:
            params['Dependencia'] = dependencia
        if serie:
            params['Serie'] = serie
        if subserie:
            params['Subserie'] = subserie
        query, _ = self.query('trd_tipodoc', params)
        rows = self.serialize(query)
        result = []
        for row in rows:
            result.append({'codigo': row['Cod'], 'nombre': row['Nombre']})
        return self.response(result)
