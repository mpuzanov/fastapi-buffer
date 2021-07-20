from fastapi.testclient import TestClient
from backend.buffer.main import app
import xml.etree.ElementTree as ET
import pytest
from .conftest import user

test_data = [  # town_id
    1,
]


class TestApi:

    def setup(self):
        self.client = TestClient(app)
        print('setup')

    @staticmethod
    def teardown():
        print('teardown')
        pass

    def test_get_tips(self):
        response = self.client.get("/api/tips", auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("tip"))
        assert root.tag == 'tips'
        assert len(items) > 0

    def test_get_finperiods(self):
        response = self.client.get("/api/finperiods", auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("finperiod"))
        assert root.tag == 'finperiods'
        assert len(items) > 0

    def test_get_suppliers(self):
        response = self.client.get("/api/suppliers", auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("supplier"))
        assert root.tag == 'suppliers'
        assert len(items) > 0

    def test_get_towns(self):
        response = self.client.get("/api/towns", auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("town"))
        assert root.tag == 'towns'
        assert len(items) > 0

    @pytest.mark.parametrize('town_id', test_data)
    def test_get_streets(self, town_id: int):
        p = {'town_id': town_id}
        response = self.client.get("/api/streets", params=p, auth=user)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/xml"
        root = ET.fromstring(response.text)
        items = list(root.iter("street"))
        assert root.tag == 'streets'
        assert len(items) > 0
