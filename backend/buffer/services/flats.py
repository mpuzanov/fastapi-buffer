from typing import (
    List,
    Optional,
)
from sqlalchemy import text
import backend.buffer.config as cfg
from .common import BaseServices
from backend.buffer.models.common import Formats


class FlatService(BaseServices):
    """ Список помещений"""

    async def get_xml(self, tip_id: int,
                      build_id: Optional[int] = None,
                      format: Formats = Formats.xml) -> Optional[str]:
        data = cfg.HEADER_XML if format == Formats.xml else ''
        sql = "EXEC rep_ivc_flats @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        params = {'tip_id': tip_id, 'build_id': build_id, 'format': format.value}
        t = text(sql)
        return self._get_execute_result(t, params, data)
