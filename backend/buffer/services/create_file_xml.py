"""
Тестируем создание xml файла
rep_ivc_pd @fin_id=231, @tip_id=2,@build_id=6765, @sup_id=null, @occ=null
"""

from sqlalchemy import create_engine, text
from fastapi import Depends
from pathlib import Path
import xml.etree.ElementTree as ET
import csv
import sys

from pydantic import errors
# sys.path.append(r'H:/MyProjects/Python/fastapi-buffer')
import backend.buffer.config as cfg

# from sqlalchemy.orm import Session
# from backend.buffer.database import Session, get_session

xml = """
<?xml version="1.0"?>
<platezhki period="2021.05">
  <item poluchatel="ООО &quot;ИВЦ-Ижевск&quot;, 426000, г. Ижевск, ул. И. Закирова, дом.3, каб. 1, ИНН: 1841008627" 
  rekvizity="Сбербанк Удмуртское отделение №8618 БИК: 049401601, р/сч: 40702810268000010356, к/сч: 30101810400000000601" 
  platelshik="Камаев А.Ф." 
  nomerls="210042076" 
  lc_numer="210042076" 
  pomeshenie="г.Ижевск, ул. Ракетная д.42 кв.76" 
  uk_rekvizity="426063, УР, Ижевск, Ордженикидзе, дом 2, ИНН: 1835012826" 
  ki_passport="" ki_buhgalteria="" ki_dispetcher="" ki_avaria="" ki_uchastor="" 
  obshaya_ploshad="25.8" 
  zaregistrirovano="2" 
  prozhivaet="пост.:2" 
  nachisleno="921.49" 
  nachisleno_uslugi="916.86" 
  nachisleno_peni="4.63" 
  nachalniy_ostatok="2065.6" 
  oplacheno="0" 
  koplate="2994.41" 
  ean_2d="ST00012|Name=ООО &quot;ИВЦ-Ижевск&quot;|PersonalAcc=40702810268000010356|BankName=Сбербанк Удмуртское отделение №8618|BIC=049401601|CorrespAcc=30101810400000000601|PayeeINN=1841008627|PersAcc=210042076|Sum=299441|PayerAddress=Г.ИЖЕВСК, УЛ. РАКЕТНАЯ Д.42 КВ.76|PaymPeriod=0521|LastName=КАМАЕВ|FirstName=А.|MiddleName=Ф.|UIN=20МВ875415-07-1051|TechCode=02" 
  pay_rs="40702810268000010356" 
  pay_ks="30101810400000000601" 
  pay_bik="049401601" 
  pay_inn="1841008627" 
  pay_kpp="183101001" 
  pay_bank="Сбербанк Удмуртское отделение №8618" 
  pay_dest="ООО &quot;ИВЦ-Ижевск&quot;" 
  typels="">
    <nachislenie 
    vid="ГВ для сод. о.и.*" 
    tarif="145,97" 
    ed="м2" 
    normativ="0" 
    potrebleno="-1,4403" 
    nachisleno="-210,24" 
    pereraschet="187,05" 
    koplate="-23,19"/>
    <nachislenie vid="Горячее водоснабжение" tarif="145,97" ed="м3" normativ="3,22" potrebleno="6,44" nachisleno="940,05" pereraschet="0" koplate="940,05"/>
  </item>
</platezhki>

"""


class XmlKvitancia:
    sql_pd: str = "rep_ivc_pd @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    sql_pd_serv: str = "rep_ivc_pd_serv @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    xml_text: str = ''
    params: dict = {}

    def __init__(self, conn, tip_id: int, build_id: int, fin_id: int, sup_id: int = 0):
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
                ET.SubElement(root_item, 'nachislenie', vid=row_detail.vid
                              , tarif=row_detail.tarif
                              , ed=row_detail.ed
                              , normativ=row_detail.normativ
                              , potrebleno=row_detail.potrebleno
                              , nachisleno=row_detail.nachisleno
                              , pereraschet=row_detail.pereraschet
                              , koplate=row_detail.koplate
                              )

        indent_xml(root)
        self.xml_text = ET.tostring(root, encoding="utf-8", method="xml", xml_declaration=True).decode(encoding="utf-8")
        # self.xml_text = ET.tostring(root, encoding="utf-8", method="xml", xml_declaration=True)
        # self.xml_text = ET.tostring(root, encoding='unicode', method='xml', xml_declaration=True)  # cp1251
        print(self.xml_text)


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


def create_xml():
    """ https://habr.com/ru/post/519604/ """

    path: Path = Path("H:/MyProjects/Python/fastapi-buffer/backend")

    # filename: Path = Path("data.csv")
    # fullname = path / filename
    # with open(fullname, encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     list_result = [row for row in reader]
    #     print(list_result)

    params = {'tip_id': 2, 'build_id': 6765,
              'fin_id': 232, 'sup_id': 0, }
    sql_pd: str = "rep_ivc_pd @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"
    sql_pd_serv: str = "rep_ivc_pd_serv @fin_id=:fin_id, @tip_id=:tip_id, @build_id=:build_id, @sup_id=:sup_id"

    engine = create_engine(cfg.settings.database_url)
    conn = engine.connect()

    t = text(sql_pd)
    result = conn.execute(t, params)
    rows = result.fetchall()

    t = text(sql_pd_serv)
    result = conn.execute(t, params)
    rows_detail = result.fetchall()
    # print(rows_detail)

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
            ET.SubElement(root_item, 'nachislenie', vid=row_detail.vid
                          , tarif=row_detail.tarif
                          , ed=row_detail.ed
                          , normativ=row_detail.normativ
                          , potrebleno=row_detail.potrebleno
                          , nachisleno=row_detail.nachisleno
                          , pereraschet=row_detail.pereraschet
                          , koplate=row_detail.koplate
                          )

    # print(ET.tostring(root, encoding="utf-8", method="xml").decode(encoding="utf-8"))
    indent_xml(root)
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    # print(xml_str.decode(encoding="utf-8"))

    etree = ET.ElementTree(root)
    file_xml = path / 'test_create_file.xml'
    with open(file_xml, "wb") as file:
        etree.write(file, encoding='utf-8', xml_declaration=True)
        # file.write(xml_str.decode(encoding="utf-8"))
