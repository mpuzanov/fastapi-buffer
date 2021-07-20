from fastapi import Query
from enum import Enum


class Formats(Enum):
    """Форматы вывода информации"""
    xml = 'xml'
    json = 'json'


class ServicesPU(Enum):
    """Услуги по счётчикам"""
    hvod = 'хвод'
    gvod = 'гвод'
    otop = 'отоп'
    gas = 'пгаз'
    elec = 'элек'


# ServicesPU = {'хвод', 'гвод', 'отоп', 'пгаз', 'элек'}


class CommonQueryParams:
    """ Входные параметры для запросов """

    __slots__ = 'tip_id', 'build_id', 'fin_id', 'sup_id', 'format'

    def __init__(self, tip_id: int = Query(..., description="Код организации"),
                 build_id: int = Query(None, description="Код дома"),
                 fin_id: int = Query(
                     None, description="Код финансового периода"),
                 sup_id: int = Query(None, description="Код поставщика"),
                 format: Formats = Query(Formats.xml, description="Формат вывода информации"),
                 ):
        self.tip_id = tip_id
        self.build_id = build_id
        self.fin_id = fin_id
        self.sup_id = sup_id
        self.format = format

    def get_dict_params(self):
        """ получение значений в виде словаря """
        return {'tip_id': self.tip_id, 'build_id': self.build_id, 'fin_id': self.fin_id, 'sup_id': self.sup_id,
                'format': self.format.value}
