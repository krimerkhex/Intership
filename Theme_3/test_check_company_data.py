import pytest
import requests
from random import randint

from urls import COMPANY_DATA_URL, COMPANY_IDS_URL


def get_company_ids():
    response = requests.get(url=COMPANY_IDS_URL, params={"code": randint(0, 3), "limit": 20})
    if response.status_code == 200:
        return response.json()
    else:
        return []


@pytest.mark.parametrize("company_id", get_company_ids())
def test_check_company_data_existence(company_id):
    response = requests.get(url=COMPANY_DATA_URL, params={"id_company": int(company_id)})
    assert response.status_code == 200
    assert len(response.json()) != 0
