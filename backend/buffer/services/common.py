from typing import (
    List,
    Optional,
)
from fastapi import (
    Depends,
    HTTPException,
)

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_session
from ..config import logger
from ..models import Formats


class BaseServices:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _execute(self, query, params=None):
        """ Возвращаем курсор выполнения запроса"""
        try:
            result = self.session.execute(text(query), params)
        except SQLAlchemyError as ex:
            error = f"{__class__.__name__} {ex}"
            logger.error(error)
            raise HTTPException(
                status_code=500,
                detail=error,
            )
        return result

    def _get_execute_result(self, query, params=None) -> str:
        """ Возвращаем значение поля result из запроса"""
        data = ''
        try:
            result = self.session.execute(text(query), params)
            rows = result.fetchone()
            if rows['result']:
                data = rows['result']
        except SQLAlchemyError as ex:
            error = f"{__class__.__name__} {ex}"
            logger.error(error)
            raise HTTPException(
                status_code=500,
                detail=error,
            )
        return data

    def get_execute_query(self, query: str, params: dict = None) -> List[dict]:
        """ Возвращаем список словарей результат выполнения запроса"""
        try:
            result = list(self.session.execute(text(query), params))
            list_dict = [{key: value for (key, value) in dict(row).items()} for row in result]
        except SQLAlchemyError as ex:
            error = f"{__class__.__name__} {ex}"
            logger.error(error)
            raise HTTPException(
                status_code=500,
                detail=error,
            )
        return list_dict


class TipService(BaseServices):
    """ Список организаций (типов жилого фонда) """

    async def get_xml(self, format: Formats = Formats.xml) -> Optional[str]:
        if format == Formats.xml:
            sql = """
                SELECT '<?xml version="1.0" encoding="UTF-8"?>'+ (
                    SELECT id as tip_id, name, fin_id, start_date, tip_uid FROM VOcc_types 
                    FOR XML RAW ('tip'), ROOT ('tips')
                ) as result
                """
        else:
            sql = """
                SELECT (
                    SELECT id as tip_id, name, fin_id, start_date, tip_uid FROM VOcc_types 
                    FOR JSON PATH, ROOT ('tips')
                ) as result
                """
        return self._get_execute_result(sql, None)


class FinService(BaseServices):
    """ Список фин.периодов """

    async def get_xml(self, format: Formats = Formats.xml) -> Optional[str]:
        if format == Formats.xml:
            sql = """
            SELECT '<?xml version="1.0" encoding="UTF-8"?>'+ (
                SELECT fin_id, start_date, StrMes FROM Global_values finperiod ORDER BY fin_id DESC
                FOR XML AUTO, ROOT ('finperiods')
            ) as result
            """
        else:
            sql = """
            SELECT (
                SELECT fin_id, start_date, StrMes FROM Global_values ORDER BY fin_id DESC
                FOR JSON PATH, ROOT ('finperiods')
            ) as result
            """
        return self._get_execute_result(sql, None)


class SupService(BaseServices):
    """ Список поставщиков с отдельной квитанцией """

    async def get_xml(self, format: Formats = Formats.xml) -> Optional[str]:
        if format == Formats.xml:
            sql = """
            SELECT '<?xml version="1.0" encoding="UTF-8"?>'+ (
                SELECT id as sup_id, name, sup_uid FROM View_suppliers_all WHERE account_one=1
                FOR XML RAW ('supplier'), ROOT ('suppliers')
            ) as result
            """
        else:
            sql = """
            SELECT (
                SELECT id as sup_id, name, sup_uid FROM View_suppliers_all WHERE account_one=1
                FOR JSON PATH, ROOT ('suppliers')
            ) as result
            """
        return self._get_execute_result(sql, None)


class TownService(BaseServices):
    """ Список населённых пунктов """

    sql = """SELECT * FROM towns"""
    sql_xml = """SELECT '<?xml version="1.0" encoding="UTF-8"?>'+ 
    (SELECT * FROM towns town FOR XML AUTO, ROOT ('towns')) as result"""
    sql_json = """SELECT (SELECT * FROM towns FOR JSON PATH, ROOT ('towns')) as result"""

    async def get_cursor(self):
        return self.get_execute_query(self.sql)

    async def get_xml(self, format: Formats = Formats.xml) -> Optional[str]:
        if format == Formats.xml:
            sql = self.sql_xml
        else:
            sql = self.sql_json
        return self._get_execute_result(sql, None)


class StreetService(BaseServices):
    """ Список улиц """

    sql = """SELECT * FROM VStreets where town_id=:town_id"""
    sql_xml = """SELECT '<?xml version="1.0" encoding="UTF-8"?>'+ (SELECT * FROM VStreets street where town_id=:town_id 
    FOR XML AUTO, ROOT ('streets')) as result"""
    sql_json = """SELECT (SELECT * FROM VStreets where town_id=:town_id FOR JSON PATH, ROOT ('Streets')) as result"""

    async def get_cursor(self, town_id: int = 1):
        return self.get_execute_query(self.sql, params={'town_id': town_id})

    async def get_xml(self, town_id: int = 1, format: Formats = Formats.xml) -> Optional[str]:
        if format == Formats.xml:
            sql = self.sql_xml
        else:
            sql = self.sql_json
        return self._get_execute_result(sql, params={'town_id': town_id})
