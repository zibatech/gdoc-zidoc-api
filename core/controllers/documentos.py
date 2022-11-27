from core.constants import EXCLUDED_FROM_DOCUMENTS
from core.controller import Controller


class DocumentosController(Controller):

    def get(self, params):
        params_dict = params.to_dict()
        if 'Asunto' in params_dict:
            params_dict['%Asunto'] = params_dict.pop('Asunto')
        result, table = self.query('documentos', params_dict)
        if type(result) == dict and result.get('error'):
            return result
        records = []
        for row in result:
            field = dict(row)
            for key in EXCLUDED_FROM_DOCUMENTS:
                del field[key]
            tipodoc = field.get('TipoDoc')
            if tipodoc != "9":
                tipodoc_res, _ = self.query('trd_tipodoc', {'Cod': tipodoc})
                tipodoc_row = dict(tipodoc_res.first())
                field['TipoDoc'] = f"{tipodoc_row['Cod']} - {tipodoc_row['Nombre']} "
            records.append(dict(field))
        return self.response(records)
