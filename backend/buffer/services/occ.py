from typing import (
    Optional,
)
from .common import BaseServices
from ..config import logger


class OccService(BaseServices):

    async def get_xml(self, **params) -> Optional[str]:
        sql = "EXEC rep_ivc_occ @tip_id=:tip_id, @fin_id=:fin_id, @build_id=:build_id, @debug=0, @format=:format"
        logger.debug(f'{__class__.__name__} {params}')
        return self._get_execute_result(sql, params)
