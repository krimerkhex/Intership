import pytest
from fastapi.testclient import TestClient
from fastapi_server import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, -1, -2),
    (1.5, 2.5, 4.0),
    (1e6, 2e6, 3e6),
])
def test_sum_numbers(a, b, expected, client):
    response = client.get(f"/calc/sum?a={a}&b={b}")
    assert response.status_code == 200
    assert response.json()["result"] == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 6),
    (0, 5, 0),
    (-2, 3, -6),
    (0.5, 4, 2.0),
])
def test_multiply_numbers(a, b, expected, client):
    response = client.get(f"/calc/multiply?a={a}&b={b}")
    assert response.status_code == 200
    assert response.json()["result"] == expected


@pytest.mark.parametrize("a,b,expected", [
    (6, 3, 2),
    (1, 2, 0.5),
    (-4, 2, -2),
    (0, 1, 0),
])
def test_divide_numbers(a, b, expected, client):
    response = client.get(f"/calc/divide?a={a}&b={b}")
    assert response.status_code == 200
    assert response.json()["result"] == expected


def test_divide_by_zero(client):
    response = client.get("/calc/divide?a=1&b=0")
    assert response.status_code == 400
    assert "Zero division error" in response.json()["detail"]


@pytest.mark.parametrize("endpoint", ["sum", "multiply", "divide"])
@pytest.mark.parametrize("params", [
    "a=abc&b=2",
    "a=1",
    "",
])
def test_invalid_input(endpoint, params, client):
    response = client.get(f"/calc/{endpoint}?{params}")
    assert response.status_code == 422
