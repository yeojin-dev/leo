import os

import pytest

from app import (
    BASE_FOLDER,
    app,
    db,
)


@pytest.fixture
def client():
    upload_path = os.path.join(BASE_FOLDER, os.environ['UPLOAD_FOLDER'])
    os.makedirs(upload_path, exist_ok=True)

    client = app.test_client()
    yield client
    db.homework.remove({})
