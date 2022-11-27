from sqlalchemy import Table
from sqlalchemy.sql.functions import concat

from core.controller import Controller


class ExpedientesController(Controller):

    def get(self, params=None):
        if params is None:
            params = {}
        trd_dependencia = Table('trd_dependencia', self.meta, autoload=True)
        trd_serie = Table('trd_serie', self.meta, autoload=True)
        trd_subserie = Table('trd_subserie', self.meta, autoload=True)
        usuarios = Table('usuarios', self.meta, autoload=True)
        pasdict = params.to_dict()
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
