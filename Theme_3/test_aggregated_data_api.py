import pytest
import requests

from urls import AGGREGATED_DATA_URL
from itertools import product


def get_variants_v1() -> list[dict]:
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


def get_variants_v2() -> list[dict]:
    codes = (0, 1, 2, 3)
    type_companies = ("ordinary", "strategist")
    flag_filters = (True, False)
    methods = ("debt_burden", "m104", "sii")

    return [
        {
            "code": code,
            "type_companies": type_company,
            "flag_filter": flag_filter,
            "method": method
        }
        for code in codes
        for type_company in type_companies
        for flag_filter in flag_filters
        for method in methods
    ]


def get_variants_v3() -> list[dict]:
    codes = (0, 1, 2, 3)
    type_companies = ("ordinary", "strategist")
    flag_filters = (True, False)
    methods = ("debt_burden", "m104", "sii")

    return [
        {
            "code": code,
            "type_companies": type_company,
            "flag_filter": flag_filter,
            "method": method
        }
        for code, type_company, flag_filter, method in product(
            codes, type_companies, flag_filters, methods
        )
    ]


@pytest.mark.parametrize("data", get_variants_v2())
def test_get_aggregated_data_different_parameters(data):
    response = requests.get(url=AGGREGATED_DATA_URL, params=data)
    assert response.status_code == 200
    assert len(response.json()) != 0
