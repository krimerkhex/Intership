import pytest
import requests

from urls import MAIN_DATA_URL, COMPANY_IDS_URL, AGGREGATED_DATA_URL


def all_regions() -> list:
    response = requests.get(url=MAIN_DATA_URL)
    regions = []
    response = response.json()
    for region in response:
        if region.get("region", ""):
            regions.append({"region": region["region"]})
    return regions


def get_company_list(record: dict, limit: int = -1):
    parameters = {"code": record["code"],
                  "type_companies": record["type_companies"],
                  "limit": limit,
                  "cascade_method": record["cascade_method"]
                  }
    if record["region"] != "Все регионы":
        parameters["region"] = record["region"],
    response = requests.get(url=COMPANY_IDS_URL,
                            params=parameters)
    return response


def get_region_info(url: str, region: dict = {}):
    data_response = requests.get(url=url, params=region)
    assert data_response.status_code == 200
    data_response = data_response.json()
    assert len(data_response) != 0
    return data_response


REGIONS = all_regions()


@pytest.mark.parametrize("region", REGIONS)
def test_check_company_count(region: dict):
    data = get_region_info(MAIN_DATA_URL, region)
    for record in data:
        companies_response = get_company_list(record)
        assert len(companies_response.json()) == (record["number_companies"] - 1)


def test_check_aggregated_company_count():
    data = get_region_info(AGGREGATED_DATA_URL)
    for record in data:
        companies_response = get_company_list(record)
        assert len(companies_response.json()) == (record["number_companies"] - 1)
