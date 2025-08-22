import pytest
import requests

from urls import MAIN_DATA_URL


def test_main_data_empty_request():
    response = requests.get(MAIN_DATA_URL)
    assert response.status_code == 200
    assert len(response.json()) != 0


@pytest.mark.parametrize("param,value", [
    ("region", "укпупк"),
    ("region", 1325646)
])
def test_non_existing_region(param, value):
    response = requests.get(url=MAIN_DATA_URL, params={param: value})
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("param,value", [
    ("region", "Республика Татарстан"),
    ("region", "Приморский край"),
    ("region", "Тверская область"),
    ("region", "Кировская область")
])
def test_existing_region(param, value):
    response = requests.get(url=MAIN_DATA_URL, params={param: value})
    assert response.status_code == 200
    assert len(response.json()) != 0
