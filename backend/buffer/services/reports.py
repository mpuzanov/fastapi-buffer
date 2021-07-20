from io import BytesIO

from .common import BaseServices
from ..utils_format import excel2003
from ..config import logger


class ReportsService(BaseServices):

    async def export_pu_xls(self, params) -> BytesIO:
        query = '''exec rep_counter_exp 
        @tip_str=:tip_str, @fin_id1=:fin_id, @build_id1=:build_id, @service_id1=:service_id
        '''
        logger.debug(f'query: {query}, params: {params}')

        query_result = self.get_execute_query(query, params)

        logger.debug(f'query_result len: {len(query_result)}')

        # список полей с наименованиями для вывода
        columns = {
            'row_num': '№ п/п',
            'occ': 'Лицевой счёт',
            'street': 'Улица',
            'nom_dom': 'Дом',
            'Корпус': 'Корпус',
            'nom_kvr': 'Квартира',
            'type': 'Тип',
            'serial_number': 'Серийный номер',
            'date_create': 'Дата установки',
            'PeriodCheck': 'Период поверки',
            'value_pred': 'Показания предыдущие',
            'Показания предыдущие (ночь)': 'Показания предыдущие (ночь)',
            'inspector_value': 'Текущие показания',
            'Показания текущие (ночь)': 'Показания текущие (ночь)',
            'inspector_date': 'Дата текущих показаний',
            'actual_value': 'Фактический расход',
            'Фактический расход (ночь)': 'Фактический расход (ночь)',
        }

        file = excel2003.query_to_excel2003(query_result,
                                            sheet_name='Лист 1',
                                            startrow=6,
                                            columns=columns
                                            )
        return file
