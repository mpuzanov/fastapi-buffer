from typing import (
    Optional,
)
from sqlalchemy import text
from ..config import logger
from .common import BaseServices
from backend.buffer.models.common import Formats
import xml.etree.ElementTree as ET


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
    xml_text: str = ''
    params: dict = {}

    def __init__(self, conn, tip_id: int, build_id: int = None, fin_id: int = None, sup_id: int = 0):
        self.params = {'tip_id': tip_id, 'build_id': build_id, 'fin_id': fin_id, 'sup_id': sup_id}
        self.conn = conn
        self._create_xml()

    def get_xml(self):
        return self.xml_text

    def _create_xml(self):

        t = text(self.sql_pd)
        result = self.conn.execute(t, self.params)
        rows = result.fetchall()

        t = text(self.sql_pd_serv)
        result = self.conn.execute(t, self.params)
        rows_detail = result.fetchall()

        count_period = 0
        root = ET.Element('platezhki')
        for row in rows:
            # print(row.period)
            if count_period == 0:
                root.set('period', row.period)
                count_period += 1

            root_item = ET.SubElement(root, 'item', num_pd=row.num_pd,
                                      rekvizity=row.rekvizity, poluchatel=row.poluchatel,
                                      platelshik=row.platelshik,
                                      nomerls=row.nomerls,
                                      lc_numer=row.lc_numer,
                                      pomeshenie=row.pomeshenie,
                                      uk_rekvizity=row.uk_rekvizity,
                                      # ki_passport="" ki_buhgalteria="" ki_dispetcher="" ki_avaria="" ki_uchastor=""
                                      obshaya_ploshad=str(row.obshaya_ploshad),
                                      zaregistrirovano=str(row.zaregistrirovano),
                                      prozhivaet=str(row.prozhivaet),
                                      nachisleno=str(row.nachisleno),
                                      nachisleno_uslugi=str(row.nachisleno_uslugi),
                                      nachisleno_peni=str(row.nachisleno_peni),
                                      nachalniy_ostatok=str(row.nachalniy_ostatok),
                                      oplacheno=str(row.oplacheno),
                                      koplate=str(row.koplate),
                                      ean_2d=row.ean_2d,
                                      pay_rs=row.pay_rs,
                                      pay_ks=row.pay_ks,
                                      pay_bik=row.pay_bik,
                                      pay_inn=row.pay_inn,
                                      pay_kpp=row.pay_kpp,
                                      pay_bank=row.pay_bank,
                                      pay_dest=row.pay_dest,
                                      typels=row.typels
                                      )
            res_ls = [d for d in rows_detail if d["nomerls"] == row.nomerls]
            # print(res_ls)
            for row_detail in res_ls:
                ET.SubElement(root_item, 'nachislenie',
                              vid=row_detail.vid,
                              tarif=row_detail.tarif,
                              ed=row_detail.ed,
                              normativ=row_detail.normativ,
                              potrebleno=row_detail.potrebleno,
                              nachisleno=row_detail.nachisleno,
                              pereraschet=row_detail.pereraschet,
                              koplate=row_detail.koplate,
                              )

        indent_xml(root)
        self.xml_text = ET.tostring(root, encoding="utf-8", method="xml", xml_declaration=True).decode(encoding="utf-8")
        # self.xml_text = ET.tostring(root, encoding="utf-8", method="xml", xml_declaration=True)
        # self.xml_text = ET.tostring(root, encoding='unicode', method='xml', xml_declaration=True)  # cp1251
        logger.debug(self.xml_text)


def indent_xml(elem, level=0):
    """ pretty-print xml """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent_xml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
