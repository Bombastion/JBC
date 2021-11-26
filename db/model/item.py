from typing import Dict

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db.model.sqlalchemy_base import Base

class Item(Base):
    __tablename__ = 'item'

    item_id = sa.Column(UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    collection_id = sa.Column(UUID, nullable=False)
    item_type_id = sa.Column(UUID, nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"Item(item_id={self.item_id}, collection_id={self.collection_id}, item_type_id={self.item_type_id}, quantity={self.quantity})"

    def to_dict(self) -> Dict:
        return {
            "item_id": str(self.item_id),
            "collection_id": str(self.collection_id),
            "item_type_id": str(self.item_type_id),
            "quantity": self.quantity,
        }