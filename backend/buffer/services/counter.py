from typing import (
    Optional,
)
from .common import BaseServices


class CounterService(BaseServices):

    async def get_xml(self, **params) -> Optional[str]:
        sql = "EXEC rep_ivc_counter @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        return self._get_execute_result(sql, params)
