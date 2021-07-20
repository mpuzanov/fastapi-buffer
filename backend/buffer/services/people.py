from typing import (
    Optional,
)
from .common import BaseServices


class PeopleService(BaseServices):

    async def get_xml(self, **params) -> Optional[str]:
        sql = "EXEC rep_ivc_people @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        return self._get_execute_result(sql, params)


class PeoplePeriodService(BaseServices):

    async def get_xml(self, **params) -> str:
        sql = "EXEC rep_ivc_people_period @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @format=:format"
        return self._get_execute_result(sql, params)