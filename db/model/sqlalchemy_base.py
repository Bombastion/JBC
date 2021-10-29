import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = sa.create_engine("postgresql://jbc:jbc@localhost:5432/jbc")
connection = engine.connect()
metadata = sa.MetaData()

SessionFactory = sessionmaker(bind=engine)