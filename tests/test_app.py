import pytest
from page_analyzer.scripts.migrations.init_db import scheme_from_file
from page_analyzer.app import app


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
    assert response.status_code == 200


def test_urls_get(client):
    response = client.get("/urls")
    assert response.status_code == 200


def test_get_url_page_correct(client):
    response = client.get("/urls/1")
    assert response.status_code == 200


def test_get_url_page_wrong(client):
    response = client.get("/urls/100")
    assert response.status_code == 404 


def test_add_page_emty(client):
    response = client.post('/urls', data={
        'url': '',
    })
    assert response.status_code == 402


def test_add_page_bad(client):
    response = client.post('/urls', data={
        'url': 'bad///url',
    })
    assert response.status_code == 402


def test_add_page_correct(client):
    response = client.post('/urls', data={
        'url': 'https://flask.palletsprojects.com/en/2.2.x/testing/',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'https://flask.palletsprojects.com' in str(response.data)

    
def test_post_check_page(client):
    response = client.post('/urls/1/checks', data={
        'url': 'https://flask.palletsprojects.com/en/2.2.x/testing/',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Страница успешно проверена' in response.text
""" 
Метод	Маршрут	Шаблон	Описание
GET	/schools	schools/index.html	Список школ
GET	/schools/{id}	schools/show.html	Информация о школе
GET	/schools/new	schools/new.html	Форма создания новой школы
POST	/schools		Создание новой школы
GET	/schools/{id}/edit	schools/edit.html	Форма редактирования школы
PATCH/PUT	/schools/{id}		Обновление школы
DELETE	/schools/{id}		Удаление школы """
