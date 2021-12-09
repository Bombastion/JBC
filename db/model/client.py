from typing import Dict

from flask_login import UserMixin
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db.model.sqlalchemy_base import Base

class Client(UserMixin, Base):
    __tablename__ = "client"
    client_id = sa.Column(UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.Text, nullable=False)
    password = sa.Column(sa.Text, nullable=False)

    def __repr__(self) -> str:
        return f"Client(client_id={self.client_id}, name={self.name}, email={self.email})"

    def to_dict(self) -> Dict:
        return {
            "client_id": str(self.client_id),
            "email": self.email,
            "name": self.name,
        }