from fastapi.testclient import TestClient
from backend.buffer.main import app
import xml.etree.ElementTree as ET
import pytest
from .conftest import user

test_data = [   # tip_id, build_id, fin_id, sup_id
    (1, 6786, None, None),
    (1, 6785, None, 345),
]


@pytest.mark.parametrize('tip_id, build_id, fin_id, sup_id', test_data)
class TestApi:

    def setup(self):
        self.client = TestClient(app)
        print('setup')

    @staticmethod
    def teardown():
        print('teardown')
        pass

    def test_get_buildings(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get("/api/buildings", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("dom"))
        assert root.tag == 'doma'
        assert len(items) > 0

    def test_get_flats(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/flats", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("pomeshenie"))
        assert root.tag == 'pomesheniya'
        assert len(items) > 0

    def test_get_occ(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/occ", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("lic_chet"))
        assert root.tag == 'licevie_scheta'
        assert len(items) > 0

    def test_get_people(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/people", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("zhitel"))
        assert root.tag == 'zhiteli'
        assert len(items) > 0

    def test_get_people_period(self, tip_id, build_id, sup_id, fin_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/people_period", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        # root = ET.fromstring(response.text)
        # items = list(root.iter("registraciya"))
        # assert root.tag == 'registracii'
        # assert len(items) > 0

    def test_get_counter(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/counter", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("shetchik"))
        assert root.tag == 'shetchiki'
        assert len(items) > 0

    def test_get_counter_value(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/counter_value", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("pokazanie"))
        assert root.tag == 'pokazaniya'
        assert len(items) > 0

    def test_get_value(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/value", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("nachislenie_LC"))
        assert root.tag == 'nachisleniya'
        assert len(items) > 0

    def test_get_pay(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/pay", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("oplata_LC"))
        assert root.tag == 'oplati'
        assert len(items) > 0

    def test_get_dolg(self, tip_id, build_id, fin_id, sup_id):
        p = {'tip_id': tip_id, 'build_id': build_id,
             'fin_id': fin_id, 'sup_id': sup_id}
        response = self.client.get(
            "/api/dolg", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("dolg_lc"))
        assert root.tag == 'dolgi'
        assert len(items) > 0
