from fastapi.testclient import TestClient
from src.api import app
from src.config import API_KEY

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_sem_api_key():
    response = client.post(
        "/otimizar",
        json={
            "comprimento_padrao": 3000,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 1000,
                    "quantidade": 2
                }
            ]
        }
    )

    assert response.status_code == 403


def test_api_key_invalida():
    response = client.post(
        "/otimizar",
        headers={
            "X-API-Key": "errada"
        },
        json={
            "comprimento_padrao": 3000,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 1000,
                    "quantidade": 2
                }
            ]
        }
    )

    assert response.status_code == 403


def test_com_api_key():
    response = client.post(
        "/otimizar",
        headers={
            "X-API-Key": API_KEY
        },
        json={
            "comprimento_padrao": 3000,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 1000,
                    "quantidade": 2
                }
            ]
        }
    )

    assert response.status_code == 200

def test_item_maior_que_barra():
    response = client.post(
        "/otimizar",
        headers={"X-API-Key": API_KEY},
        json={
            "comprimento_padrao": 3000,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 4000,
                    "quantidade": 1
                }
            ]
        }
    )

    assert response.status_code == 422

def test_comprimento_barra_invalido():
    response = client.post(
        "/otimizar",
        headers={"X-API-Key": API_KEY},
        json={
            "comprimento_padrao": 0,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 1000,
                    "quantidade": 2
                }
            ]
        }
    )

    assert response.status_code == 422

def test_quantidade_zero():
    response = client.post(
        "/otimizar",
        headers={"X-API-Key": API_KEY},
        json={
            "comprimento_padrao": 3000,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 1000,
                    "quantidade": 0
                }
            ]
        }
    )

    assert response.status_code == 422

def test_time_limit_invalido():
    response = client.post(
        "/otimizar",
        headers={"X-API-Key": API_KEY},
        json={
            "comprimento_padrao": 3000,
            "time_limit": 150,
            "itens": [
                {
                    "id": "A",
                    "comprimento": 1000,
                    "quantidade": 2
                }
            ]
        }
    )

    assert response.status_code == 422