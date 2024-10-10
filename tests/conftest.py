import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from madr.app import app
from madr.database import get_session
from madr.models import table_registry
from madr.security import get_password_hash
from tests.factories import BookFactory, NovelistFactory, UserFactory


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

    return novelists


@pytest.fixture
def book(session, novelist):
    db_book = BookFactory(novelist_id=novelist.id)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@pytest.fixture
def books_10(session, novelist):
    books = BookFactory.build_batch(10)

    session.bulk_save_objects(books)
    session.commit()

    return books


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserFactory(hashed_password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def token(client, user):
    response = client.post('/auth/token', data={'username': user.username, 'password': user.clean_password})
    response_json = response.json()

    return response_json.get('access_token')
