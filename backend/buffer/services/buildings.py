from backend.buffer.models.common import Formats
from backend.buffer.services.common import BaseServices
from typing import (
    Optional,
)
from sqlalchemy import text
import backend.buffer.config as cfg
from ..models import CommonQueryParams


class BuildingService(BaseServices):

    async def get_xml(self, param: CommonQueryParams) -> Optional[str]:
        data = cfg.HEADER_XML if param.format == Formats.xml else ''
        sql = "EXEC rep_ivc_buildings @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        params = {'tip_id': param.tip_id,
                  'build_id': param.build_id, 'format': param.format.value}
        t = text(sql)
        return self._get_execute_result(t, params, data)
