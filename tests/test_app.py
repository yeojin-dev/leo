import os
from http import HTTPStatus


def test_home(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_submit_homework(client):
    title = 'test html'
    author = 'tester'
    password = client.application.config['UPLOAD_PASSWORD']
    data = {'title_give': title, 'author_give': author, 'password_give': password}

    response = client.post(f'/homework', data=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json['result'] == 'success'


def test_submit_homework_with_a_wrong_password(client):
    title = 'test html'
    author = 'tester'
    password = 'wrong_password'
    data = {'title_give': title, 'author_give': author, 'password_give': password}

    response = client.post(f'/homework', data=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json['result'] == 'fail'


def test_upload_homework(client):
    title = 'test html'
    author = 'tester'
    temp_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'temp.html')

    with open(temp_filepath, 'rb') as temp_file:
        data = {'file': (temp_file, temp_file.name)}
        response = client.post(f'/homework/{author}/{title}', data=data, content_type='multipart/form-data')
    assert response.status_code == HTTPStatus.OK
