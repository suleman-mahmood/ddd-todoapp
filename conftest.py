import pytest
import psycopg2


@pytest.fixture
def connection():
    # yield psycopg2.connect("dbname=todolist")
    yield psycopg2.connect(
        user="suleman",
        password="admin",
        host="34.136.84.83",
        database="suleman",
    )
