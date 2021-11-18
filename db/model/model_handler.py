from dataclasses import dataclass
import logging
from typing import Any, List

from sqlalchemy.sql.expression import text

from db.model import Client, Item, ItemCollection, ItemType

class ItemTypeQuery:
    def __init__(self, ids: List[str]=None, text_search: str = None):
        self.ids = ids
        self.text_search = text_search

class ModelHandler:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def persist_object(self, object: Any) -> None:
        session = self.session_factory()
        session.add(object)
        session.commit()
        session.refresh(object)
        session.expunge(object)

    def delete_object(self, object: Any) -> None:
        session = self.session_factory()
        session.delete(object)
        session.commit()

    def list_item_types(self, query: ItemTypeQuery) -> List[ItemType]:
        session = self.session_factory()
        criteria = []
        if query.ids:
            criteria.append(ItemType.item_type_id.in_(query.ids))
        if query.text_search:
            criteria.append(ItemType.name.match(query.text_search))

        return session.query(ItemType).filter(*session).order_by(ItemType.item_type_id).all()
