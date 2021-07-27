from typing import (
    Optional,
)
from .common import BaseServices
from ..config import logger


class CounterService(BaseServices):

    async def get_xml(self, **params) -> Optional[str]:
        sql = "EXEC rep_ivc_counter @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        logger.debug(f'{__class__.__name__} {params}')
        return self._get_execute_result(sql, params)
