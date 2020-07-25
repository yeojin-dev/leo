import os
from http import HTTPStatus


def test_home(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_submit_and_upload_homework(client):
    title = 'test html'
    author = 'tester'
    password = client.application.config['UPLOAD_PASSWORD']
    data = {'title_give': title, 'author_give': author, 'password_give': password}

    response = client.post('/homework', data=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json['result'] == 'success'

    temp_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'temp.html')

    with open(temp_filepath, 'rb') as temp_file:
        data = {'file': (temp_file, temp_file.name)}
        response = client.post(f'/homework/{author}/{title}', data=data, content_type='multipart/form-data')
    assert response.status_code == HTTPStatus.OK


def test_read_homework(client):
    title = 'test html'
    author = 'tester'
    password = client.application.config['UPLOAD_PASSWORD']
    data = {'title_give': title, 'author_give': author, 'password_give': password}
    client.post('/homework', data=data)

    temp_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'temp.html')
    with open(temp_filepath, 'rb') as temp_file:
        temp_html: str = temp_file.read().decode()

        temp_file.seek(0)
        data = {'file': (temp_file, temp_file.name)}
        client.post(f'/homework/{author}/{title}', data=data, content_type='multipart/form-data')

    response = client.get(f'/homework/{author}/{title}')
    assert response.status_code == HTTPStatus.OK
    assert temp_html == response.data.decode()


def test_submit_homework_with_a_wrong_password(client):
    title = 'test html'
    author = 'tester'
    password = 'wrong_password'
    data = {'title_give': title, 'author_give': author, 'password_give': password}

    response = client.post('/homework', data=data)
    assert response.status_code == HTTPStatus.OK
    assert response.json['result'] == 'fail'
