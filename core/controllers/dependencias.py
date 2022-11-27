from core.controller import Controller


class DependenciasController(Controller):

    def get(self):
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
