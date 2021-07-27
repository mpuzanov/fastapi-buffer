from backend.buffer.services.common import BaseServices
from typing import (
    Optional,
)
from ..models import CommonQueryParams
from ..config import logger


class BuildingService(BaseServices):

    async def get_xml(self, param: CommonQueryParams) -> Optional[str]:
        sql = "EXEC rep_ivc_buildings @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        params = {'tip_id': param.tip_id,
                  'build_id': param.build_id, 'format': param.format.value}
        logger.debug(f'{__class__.__name__} {params}')
        return self._get_execute_result(sql, params)
