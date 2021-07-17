import copy

import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command, config as alembic_config

from app import make_app
from components.users.models import User
from utils.settings import config


@pytest.fixture(scope='session', autouse=True)
def create_db():
    original_db_name = copy.copy(config.db_name)
    config.db_name = 'postgres'
    new_engine = create_engine(config.alchemy_url)
    session = sessionmaker(bind=new_engine)()
    session.connection().connection.set_isolation_level(0)
    session.execute(f'''
        SELECT
            pg_terminate_backend(pg_stat_activity.pid)
        FROM
            pg_stat_activity
        WHERE
            pg_stat_activity.datname = '{original_db_name}' AND
        pid <> pg_backend_pid();
    ''')
    session.execute(f'drop database if exists {original_db_name}')
    session.execute(f'create database {original_db_name}')
    session.close()

    config.db_name = original_db_name

    print(f'\n Creating new database {original_db_name}')

    conf = alembic_config.Config('alembic.ini')
    conf.set_section_option('alembic', 'sqlalchemy.url', config.alchemy_url)
    print(f' Upgrading database {config.db_name}')
    command.upgrade(conf, 'head')


@pytest.fixture(scope='session', autouse=True)
def test_superuser() -> 'User':
    test_user = User.create(
        email='test-superuser@gmail.com',
        password='qwerty',
        first_name='Test',
        last_name='SuperUser',
        superuser=True
    )

    return test_user


@pytest.fixture(scope='session', autouse=True)
def test_user() -> User:
    test_user = User.create(
        email='test-user@gmail.com',
        password='qwerty',
        first_name='Test',
        last_name='User'
    )

    return test_user


@pytest.fixture(scope='module')
def server_app() -> Flask:
    return make_app()
