"""
Тестируем создание xml файла
rep_ivc_pd @fin_id=231, @tip_id=2,@build_id=6765, @sup_id=null, @occ=null
"""

from sqlalchemy import create_engine, text
from pathlib import Path
import xml.etree.ElementTree as ET
from backend.buffer.config import settings as cfg, logger
from icecream import ic


class XmlKvitancia:
    sql_pd: str = "rep_ivc_pd @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    sql_pd_serv: str = "rep_ivc_pd_serv @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    xml_text: str = ''
    params: dict = {}

    def __init__(self, conn, tip_id: int, build_id: int, fin_id: int, sup_id: int = 0):
        self.params = {'tip_id': tip_id, 'build_id': build_id, 'fin_id': fin_id, 'sup_id': sup_id}
        self.conn = conn

    def get_xml(self):
        self.xml_text = self._create_xml()
        return self.xml_text

    def _create_xml(self) -> str:

        t = text(self.sql_pd)
        result = self.conn.execute(t, self.params)
        rows = result.fetchall()
        ic(rows)
        t = text(self.sql_pd_serv)
        result = self.conn.execute(t, self.params)
        rows_detail = result.fetchall()
        logger.debug(len(rows_detail))

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
                                      occ=row.occ,
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
                                      typels=row.typels,
                                      ediny_ls=row.ediny_ls,
                                      id_jku_gis=row.id_jku_gis,
                                      size_live=row.size_live,
                                      size_other=row.size_other,
                                      size_oi_hv_gv_vo=row.size_oi_hv_gv_vo,
                                      size_oi_el=row.overdue_start,
                                      )
            res_ls = [detail for detail in rows_detail if detail["occ"] == row.occ]
            # print(res_ls)
            for row_detail in res_ls:
                ET.SubElement(root_item, 'nachislenie', vid=row_detail.vid,
                              tarif=row_detail.tarif,
                              ed=row_detail.ed,
                              normativ=row_detail.normativ,
                              potrebleno=row_detail.potrebleno,
                              nachisleno=row_detail.nachisleno,
                              pereraschet=row_detail.pereraschet,
                              koplate=row_detail.koplate,
                              )

        indent_xml(root)
        result = ET.tostring(root, encoding="utf-8", method="xml", xml_declaration=True).decode(encoding="utf-8")
        # result = ET.tostring(root, encoding="utf-8", method="xml", xml_declaration=True)
        # result = ET.tostring(root, encoding='unicode', method='xml', xml_declaration=True)  # cp1251
        ic(result)
        return result


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


if __name__ == '__main__':
    engine = create_engine(cfg.settings.database_url)
    params = {'tip_id': 2, 'build_id': 6765,
              'fin_id': 232, 'sup_id': 0}
    # create_xml()
    xml = XmlKvitancia(engine.connect(), 2, 6765, 232, 0)

    path: Path = Path("H:/MyProjects/Python/fastapi-buffer/backend")
    file_xml = path / 'test_create_file.xml'
    with open(file_xml, "w", encoding="utf-8") as file:
        file.write(xml.get_xml())
