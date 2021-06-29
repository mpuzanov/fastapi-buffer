from typing import (
    List,
    Optional,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_session
from ..config import logger
import backend.buffer.config as cfg
from ..models import Formats


class BaseServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _execute(self, sql, params=None):
        """ Возвращаем курсор выполнения запроса"""
        try:
            result = self.session.execute(sql, params)
        except SQLAlchemyError as ex:
            error = f"{__class__.__name__} {ex}"
            logger.error(error)
            raise HTTPException(
                status_code=500,
                detail=error,
            )
        return result
    
    def _get_execute_result(self, sql, params=None, data: str = '') -> str:
        """ Возвращаем значение поля result из запроса"""
        try:
            result = self.session.execute(sql, params)
            rows = result.fetchone()
            if rows['result']:
                data += rows['result']
        except SQLAlchemyError as ex:
            error = f"{__class__.__name__} {ex}"
            logger.error(error)
            raise HTTPException(
                status_code=500,
                detail=error,
            )
        return data


class TipService(BaseServices):
    """ Список организаций (типов жилого фонда) """

    async def get_xml(self, format: Formats) -> Optional[str]:
        data = ''
        if format == Formats.xml:
            data = cfg.HEADER_XML
            sql = """
                SELECT (
                    SELECT id as tip_id, name, fin_id, start_date, tip_uid FROM Occupation_Types 
                    FOR XML PATH ('tip'), ELEMENTS, ROOT ('tips')
                ) as result
                """
        else:
            sql = """
                SELECT (
                    SELECT id as tip_id, name, fin_id, start_date, tip_uid FROM Occupation_Types 
                    FOR JSON PATH, ROOT ('tips')
                ) as result
                """
        t = text(sql)
        return self._get_execute_result(t, None, data)


class FinService(BaseServices):
    """ Список фин.периодов """

    async def get_xml(self, format: Formats) -> Optional[str]:
        data = cfg.HEADER_XML if format == Formats.xml else ''
        if format == Formats.xml:
            sql = """
            SELECT (
                SELECT fin_id, start_date, StrMes FROM Global_values ORDER BY fin_id DESC
                FOR XML PATH ('finperiod'), ELEMENTS, ROOT ('finperiods')
            ) as result
            """
        else:
            sql = """
            SELECT (
                SELECT fin_id, start_date, StrMes FROM Global_values ORDER BY fin_id DESC
                FOR JSON PATH, ROOT ('finperiods')
            ) as result
            """
        t = text(sql)
        return self._get_execute_result(t, None, data)


class SupService(BaseServices):
    """ Список поставщиков с отдельной квитанцией """

    async def get_xml(self, format: Formats) -> Optional[str]:
        data = cfg.HEADER_XML if format == Formats.xml else ''
        if format == Formats.xml:
            sql = """
            SELECT (
                SELECT id as sup_id, name, sup_uid FROM Suppliers_all WHERE account_one=1
                FOR XML PATH ('Supplier'), ELEMENTS, ROOT ('Suppliers')
            ) as result
            """
        else:
            sql = """
            SELECT (
                SELECT id as sup_id, name, sup_uid FROM Suppliers_all WHERE account_one=1
                FOR JSON PATH, ROOT ('Suppliers')
            ) as result
            """
        t = text(sql)
        return self._get_execute_result(t, None, data)
