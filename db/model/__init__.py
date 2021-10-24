import sqlalchemy as sa

engine = sa.create_engine("postgresql://jbc:jbc@localhost:5432/jbc")
connection = engine.connect()
metadata = sa.MetaData()
