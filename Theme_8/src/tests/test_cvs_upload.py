import pytest

import requests


@pytest.mark.parametrize("file_path", ["test.csv"])
def test_upload_company_data(file_path):
    with open(file_path, "rb") as f:
        response = requests.post("http://localhost:8000/api/upload-csv", files={"file": f})
    assert response.status_code == 201
    assert "Info" in response.json().keys()
    assert 2 == response.json()["Info"]["Added"]
c