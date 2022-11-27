from core.controller import Controller


class UsuariosController(Controller):

    def get(self):
        query, _ = self.query('usuarios')
        rows = self.serialize(query)
        result = []
        for row in rows:
            result.append({'id': row['id'], 'nombre': row['Nombre']})
        return self.response(result)
