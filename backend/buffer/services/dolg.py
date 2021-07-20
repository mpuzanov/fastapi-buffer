from typing import (
    Optional,
)
from .common import BaseServices


class DolgService(BaseServices):

    async def get_xml(self, **params) -> Optional[str]:
        """
        params = {'tip_id': tip_id, 'build_id': build_id, 'fin_id': fin_id, 'sup_id': sup_id, 'format': format.value}
        """
        sql = """EXEC rep_ivc_dolg @fin_id=:fin_id,@tip_str=:tip_str,@sup_id=:sup_id, 
        @build_id=:build_id, @only_dolg=0, @format=:format"""
        params['tip_str'] = str(params.get('tip_id'))
        return self._get_execute_result(sql, params)
