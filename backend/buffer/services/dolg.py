from typing import (
    Optional,
)

from sqlalchemy import text
import backend.buffer.config as cfg
from .common import BaseServices
from backend.buffer.models.common import Formats


class DolgService(BaseServices):

    async def get_xml(self, tip_id: int,
                      build_id: Optional[int] = None,
                      fin_id: Optional[int] = None,
                      sup_id: Optional[int] = None,
                      format: Formats = Formats.xml) -> Optional[str]:
        data = cfg.HEADER_XML
        sql = """EXEC rep_ivc_dolg @fin_id=:fin_id,@tip_str=:tip_id,@sup_id=:sup_id, 
        @build_id=:build_id, @only_dolg=0, @format=:format"""
        params = {'tip_id': tip_id, 'build_id': build_id,
                  'fin_id': fin_id, 'sup_id': sup_id, 'format': format.value}
        t = text(sql)
        return self._get_execute_result(t, params, data)
