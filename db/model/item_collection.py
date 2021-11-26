from typing import Dict

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db.model.sqlalchemy_base import Base

class ItemCollection(Base):
    __tablename__ = "item_collection"
    collection_id = sa.Column(UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    client_id = sa.Column(UUID, nullable=False)
    name = sa.Column(sa.Text, nullable=False)

    def __repr__(self) -> str:
        return f"ItemCollection(collection_id={self.collection_id}, client_id={self.client_id}, name={self.name})"

    def to_dict(self) -> Dict:
        return {
            "collection_id": str(self.collection_id),
            "client_id": str(self.client_id),
            "name": self.name,
        }