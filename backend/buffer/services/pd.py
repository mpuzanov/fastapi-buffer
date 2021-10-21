from typing import (
    Optional,
)
from ..config import logger
from .common import BaseServices
from backend.buffer.models.common import Formats
from lxml import etree as ET
from icecream import ic
from sqlalchemy import text


class PdService(BaseServices):
    tip_id: int
    build_id: Optional[int] = None
    fin_id: Optional[int] = None
    sup_id: Optional[int] = None

    async def get_xml(self, tip_id: int,
                      build_id: Optional[int] = None,
                      fin_id: Optional[int] = None,
                      sup_id: Optional[int] = None,
                      format: Formats = Formats.xml) -> Optional[str]:

        self.tip_id = tip_id
        self.build_id = build_id
        self.fin_id = fin_id
        self.sup_id = sup_id

        if format == Formats.json:
            return ''
        else:
            return self._create_xml()

    def _create_xml(self):
        xml = XmlKvitancia(self.session, self.tip_id, self.build_id, self.fin_id, self.sup_id)
        return xml.get_xml()


class XmlKvitancia:
    sql_pd: str = "rep_ivc_pd @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    sql_pd_serv: str = "rep_ivc_pd_serv @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    sql_pd_added: str = """
    exec rep_ivc_pd_added @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id = :sup_id
    """
    sql_pd_opu: str = """
    EXEC rep_ivc_pd_opu @fin_id=:fin_id, @build_id=:build_id, @tip_id=:tip_id, @sup_id=:sup_id, @all=1   
    """
    sql_pd_norma: str = """
    exec rep_ivc_pd_norma @fin_id=:fin_id,@build_id=:build_id,@sup_id=:sup_id,@all=1
    """
    sql_pd_house: str = """
    exec rep_ivc_pd_house @fin_id=:fin_id, @build_id=:build_id
    """

    params: dict = {}

    def __init__(self, session, tip_id: int, build_id: int = None, fin_id: int = None, sup_id: int = 0):
        self.params = {'tip_id': tip_id, 'build_id': build_id, 'fin_id': fin_id, 'sup_id': sup_id}
        self.params_query = self.params
        self.session = session
        logger.debug(self.params)
        # ic(self.params)

    def get_xml(self):
        return self._create_xml()

    def _get_list_dict_from_query(self, query, params) -> list[dict]:
        result = list(self.session.execute(text(query), params=params))
        return [{key: value for (key, value) in dict(row).items()} for row in result]

    def _create_xml(self) -> str:

        rows = self._get_list_dict_from_query(self.sql_pd, self.params)
        if len(rows) == 0:
            return ''

        # ic(len(rows))
        rows_detail = self._get_list_dict_from_query(self.sql_pd_serv, self.params)
        # ic(len(rows_detail))
        rows_added = self._get_list_dict_from_query(self.sql_pd_added, self.params)
        # ic(rows_added)

        rows_norma: list[dict] = []
        rows_opu: list[dict] = []
        rows_house: list[dict] = []

        row_columns = [s for s in rows[0].keys() if s not in ['period', 'build_id']]

        build: int = 0
        count_period = 0
        root = ET.Element('platezhki')
        for row in rows:

            if row.get('build_id', 0) != build:
                build = row.get('build_id', 0)
                self.params_query['build_id'] = build
                # ic(self.params.get('sup_id'))
                if not self.params.get('sup_id'):
                    rows_norma = self._get_list_dict_from_query(self.sql_pd_norma, self.params_query)
                    # ic(len(rows_norma))
                    rows_opu = self._get_list_dict_from_query(self.sql_pd_opu, self.params_query)
                    # ic(len(rows_opu))
                    rows_house = self._get_list_dict_from_query(self.sql_pd_house, self.params_query)
                    # ic(len(rows_house))
                else:
                    rows_norma = []
                    rows_opu = []
                    rows_house = []

            if count_period == 0:
                root.set('period', row['period'])
                count_period += 1

            root_item = ET.SubElement(root, 'item')
            # for col in elem_cols:
            #     etree.SubElement(root_item, col).text = str(row.get(col))
            for col in row_columns:
                root_item.set(col, str(row.get(col)))

            # ic(len(rows_detail))
            # print(rows_detail)
            # ic(row.get('occ'))
            res_ls = [d for d in rows_detail if d['occ'] == row.get('occ')]
            # ic(len(res_ls))
            for row_detail in res_ls:
                root_detail = ET.SubElement(root_item, 'nachislenie')
                for col in ['vid', 'tarif', 'ed', 'normativ', 'potrebleno', 'nachisleno', 'pereraschet', 'koplate']:
                    root_detail.set(col, str(row_detail.get(col)))

            # ic(row.get('nomerls'))
            filter_ls = [d for d in rows_added if d["occ"] == int(row.get('occ'))]
            # ic(len(filter_ls))
            for row_detail in filter_ls:
                # ic(row_detail)
                root_detail = ET.SubElement(root_item, 'nachislenie')
                for col in ['type', 'usluga', 'osnovanie', 'summa']:
                    root_detail.set(col, str(row_detail.get(col)))

            # ========================================================================
            filter_ls = [d for d in rows_norma if d["occ"] == int(row.get('occ'))]
            for row_detail in filter_ls:
                # ic(row_detail)
                root_detail = ET.SubElement(root_item, 'nachislenie')
                for col in ['type', 'usluga', 'ed', 'ind']:
                    root_detail.set(col, str(row_detail.get(col)))

            for row_detail in rows_opu:
                # ic(row_detail)
                root_detail = ET.SubElement(root_item, 'nachislenie')
                for col in ['type', 'name', 'usluga', 'number', 'ed', 'last_value', 'last_date', 'current_value',
                            'current_date', 'rashod', 'coef']:
                    root_detail.set(col, str(row_detail.get(col)))

            for row_detail in rows_house:
                # ic(row_detail)
                root_detail = ET.SubElement(root_item, 'nachislenie')
                for col in ['type', 'usluga', 'ed', 'value_odpu', 'value_build', 'value_odn']:
                    root_detail.set(col, str(row_detail.get(col)))
            # ========================================================================

        xml_str = ET.tostring(root,
                              pretty_print=True,
                              encoding="utf-8",
                              method="xml",
                              xml_declaration=True).decode(encoding="utf-8")
        logger.debug(xml_str)
        ic('Формирование квитанции выполнено')
        return xml_str
