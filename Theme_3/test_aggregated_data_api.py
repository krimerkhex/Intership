import pytest
import requests

from urls import AGGREGATED_DATA_URL


def get_variants() -> list[dict]:
    codes = (0, 1, 2, 3)
    type_companies = ("ordinary", "strategist")
    flag_filters = (True, False)
    methods = ("debt_burden", "m104", "sii")
    data = []
    for code in codes:
        for type_company in type_companies:
            for flag_filter in flag_filters:
                for method in methods:
                    data.append(
                        {"code": code, "type_companies": type_company, "flag_filter": flag_filter, "method": method})
    return data


@pytest.mark.parametrize("data", get_variants())
def test_different_parameters(data):
    response = requests.get(url=AGGREGATED_DATA_URL, params=data)
    assert response.status_code == 200
    assert len(response.json()) != 0
