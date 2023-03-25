from http import HTTPStatus

import pytest
from page_analyzer.app import app
from page_analyzer.scripts.migrations.init_db import scheme_from_file


@pytest.fixture()
def test_app():

    # other setup can go here
    scheme_from_file()
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


def test_request_example(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_urls_get(client):
    response = client.get("/urls")
    assert response.status_code == HTTPStatus.OK


def test_get_url_page_correct(client):
    response = client.get("/urls/1")
    assert response.status_code == HTTPStatus.OK


def test_get_url_page_wrong(client):
    response = client.get("/urls/100")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_add_page_emty(client):
    response = client.post('/urls', data={
        'url': '',
    })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_page_bad(client):
    response = client.post('/urls', data={
        'url': 'bad///url',
    })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_page_correct(client):
    response = client.post('/urls', data={
        'url': 'https://flask.palletsprojects.com/en/2.2.x/testing/',
    }, follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert 'https://flask.palletsprojects.com' in str(response.data)


def test_post_check_page_bad(client):
    response = client.post('/urls/1/checks', follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert 'Произошла ошибка при проверке' in response.text


def test_post_check_page_correct(client):
    response = client.post('/urls/8/checks', follow_redirects=True)
    assert response.status_code == HTTPStatus.OK
    assert 'Страница успешно проверена' in response.text
