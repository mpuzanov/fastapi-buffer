from fastapi import Depends, Query
from pydantic import BaseModel, Field
from enum import Enum


class Formats(Enum):
    """Форматы вывода информации"""    
    xml = 'xml'
    json = 'json'


class CommonQueryParams:
    """ Входные параметры для запросов """
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
