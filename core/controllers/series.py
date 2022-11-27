from core.constants import BAD_REQUEST
from core.controller import Controller


class SeriesController(Controller):

    def get(self, params):
        dependencia = params.get('dependencia')
        if not dependencia:
            return self.response(
                {'message': 'Dependencia no especificada.'},
                BAD_REQUEST
            )
        query, table = self.query(
            'trd_serie',
            {'Dependencia': dependencia}
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
