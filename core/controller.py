from abc import ABC, abstractmethod
from os import environ as env

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker

from .constants import SUCCESS_REQUEST


class Controller(ABC):
    session = None
    meta = None

    def __init__(self):
        engine = create_engine(env['DB_URI'])
        DBSession = sessionmaker(bind=engine)
        self.meta = MetaData(engine)
        self.session = DBSession()

    def response(self, data, status=SUCCESS_REQUEST):
        ok = status < 400
        _return = {'ok': ok}
        if ok:
            _return['data'] = data
        else:
            _return |= data
        self.terminate()
        return _return, status

    def query(self, name, params=None, foreign_fields=None):
        if foreign_fields is None:
            foreign_fields = []
        if params is None:
            params = {}
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
            return (
                {'error': True, 'code': 'invalid_query', 'message': str(e)},
                None
            )

    @abstractmethod
    def get(self):
        pass

    def terminate(self):
        self.session.close()

    @staticmethod
    def serialize(result):
        return [dict(row) for row in result]
