import pytest
from fastapi.testclient import TestClient
from backend.buffer.main import app
import xml.etree.ElementTree as ET

client = TestClient(app)

test_data = [   # tip_id, build_id, fin_id, sup_id
    (1, 6786, None, None),
    (1, 6785, None, 345),
    (2, 6765, None, None)
]


@pytest.mark.parametrize('tip_id, build_id, fin_id, sup_id', test_data)
def test_read_pd(tip_id, build_id, fin_id, sup_id):
    p = {'tip_id': tip_id, 'build_id': build_id,
         'fin_id': fin_id, 'sup_id': sup_id}
    response = client.get("/api/pd", params=p)
    assert response.status_code == 200
    root = ET.fromstring(response.text)
    count_lc = 0
    # for child in root:
    #     count_lc += 1
    #     print(child.tag, child.attrib)
    #     print(child.tag, child.attrib['lc_numer'], child.attrib['nomerls'])

    items = list(root.iter("item"))
    count_lc = len(items)
    # print('count_lc=', count_lc)
    # nomerls = [child.attrib['lc_numer'] for child in root]
    # print(len(nomerls))
    assert response.headers['Content-Type'] == "application/xml"
    assert root.tag == 'platezhki'
    assert count_lc > 0


if __name__ == '__main__':
    test_read_pd()
