import pytest
from fastapi.testclient import TestClient
from backend.buffer.main import app
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from .conftest import user

client = TestClient(app)

test_data = [  # tip_id, build_id, fin_id, sup_id
    (1, 6781, None, None),
    (1, 6785, None, 345),
    (2, 6765, None, None)
]

# список атрибутов для проверки
attrib_find = ['poluchatel', 'rekvizity', 'nomerls', 'lc_numer', 'ediny_ls', 'ean_2d']


@pytest.mark.parametrize('tip_id, build_id, fin_id, sup_id', test_data)
def test_read_pd(tip_id, build_id, fin_id, sup_id):
    p = {'tip_id': tip_id, 'build_id': build_id,
         'fin_id': fin_id, 'sup_id': sup_id}
    response = client.get("/api/pd", params=p, auth=user)
    assert response.status_code == 200
    root = ET.fromstring(bytes(response.text, encoding='utf-8'))

    for attr_name in attrib_find:
        assert root.find(f'./item[@{attr_name}]') is not None, f"нет атрибута @{attr_name}"

    if p.get('sup_id') == 0:
        for attr_name in ['vid', 'tarif', 'koplate']:
            assert root.find(f'./item/nachislenie[@{attr_name}]') is not None, f"нет атрибута @{attr_name}"

    items = list(root.iter("item"))
    count_lc = len(items)
    assert response.headers['Content-Type'] == "application/xml"
    assert root.tag == 'platezhki'
    assert count_lc > 0


if __name__ == '__main__':
    test_read_pd()
