from backend.buffer.models.common import Formats
from typing import (
    Optional,
)
from sqlalchemy import text
from .common import BaseServices
import backend.buffer.config as cfg


class ValueService(BaseServices):

    async def get_xml(self, tip_id: int,
                      build_id: Optional[int] = None,
                      fin_id: Optional[int] = None,
                      format: Formats = Formats.xml) -> Optional[str]:
        data = cfg.HEADER_XML if format == Formats.xml else ''
        sql = "EXEC rep_ivc_value @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        params = {'tip_id': tip_id, 'build_id': build_id,
                  'fin_id': fin_id, 'format': format.value}
        t = text(sql)
        return self._get_execute_result(t, params, data)
