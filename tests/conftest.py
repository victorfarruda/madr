import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from madr.app import app
from madr.database import get_session
from madr.models import table_registry
from tests.factories import NovelistFactory


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg2') as p:
        _engine = create_engine(p.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def novelist(session):
    novelist = NovelistFactory()

    session.add(novelist)
    session.commit()
    session.refresh(novelist)

    return novelist


@pytest.fixture
def novelists_10(session):
    novelists = NovelistFactory.build_batch(10)

    session.bulk_save_objects(novelists)
    session.commit()

    return novelist
