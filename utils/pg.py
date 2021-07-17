from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .settings import config

engine = create_engine(config.alchemy_url)

db_session = sessionmaker(bind=engine)()

Base = declarative_base()
