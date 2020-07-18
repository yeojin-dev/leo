import pytest

from app import (
    app,
    db,
)


@pytest.fixture
def client():
    client = app.test_client()
    yield client
    db.homework.remove({})
