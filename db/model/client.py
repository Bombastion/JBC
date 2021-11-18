import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db.model.sqlalchemy_base import Base

class Client(Base):
    __tablename__ = "client"
    client_id = sa.Column(UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.Text, nullable=False)

    def __repr__(self) -> str:
        return f"Client(client_id={self.client_id}, name={self.name}, email={self.email})"
