import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from db.model.sqlalchemy_base import Base

class ItemType(Base):
    __tablename__ = 'item_type'

    item_type_id = sa.Column(UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()"))
    name = sa.Column(sa.Text, nullable=False)
    producer = sa.Column(sa.Text, nullable=True)

    def __repr__(self) -> str:
        return f"ItemType(item_type_id={self.item_type_id}, name={self.name})"
