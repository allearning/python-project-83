import pytest

from page_analyzer.app import app



@pytest.fixture()
def app_():

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app_):
    return app_.test_client()


def test_request_example(client):
    response = client.get("/")
    assert response.status_code == 200
