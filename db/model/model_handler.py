from dataclasses import dataclass
import logging
from typing import Any, List

from sqlalchemy import func
from sqlalchemy.sql.expression import text

from db.model import Client, Item, ItemCollection, ItemType

class ItemTypeQuery:
    def __init__(self, ids: List[str]=None, text_search: str=None):
        self.ids = ids
        self.text_search = text_search

class ItemQuery:
    def __init__(self, ids: List[str]=None, collection_ids: List[str]=None, item_type_ids: List[str]=None):
        self.ids = ids
        self.collection_ids = collection_ids
        self.item_type_ids = item_type_ids

class ClientQuery:
    def __init__(self, name: str=None, email: str=None, ids: List[str]=None):
        self.name = name
        self.email = email
        self.ids = ids

class CollectionQuery:
    def __init__(self, ids: List[str]=None, client_ids: List[str]=None, name: str=None):
        self.ids = ids
        self.client_ids = client_ids
        self.name = name

class ModelHandler:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def persist_object(self, object: Any) -> None:
        session = self.session_factory()
        session.add(object)
        session.commit()
        session.refresh(object)
        session.expunge(object)
        session.close()

    def delete_object(self, object: Any) -> None:
        session = self.session_factory()
        session.delete(object)
        session.commit()
        session.close()

    def list_items(self, query: ItemQuery) -> List[Item]:
        session = self.session_factory()
        criteria = []
        if query.ids:
            criteria.append(Item.item_id.in_(query.ids))
        if query.collection_ids:
            criteria.append(Item.collection_id.in_(query.collection_ids))
        if query.item_type_ids:
            criteria.append(Item.item_type_id.in_(query.item_type_ids))

        results = session.query(Item).filter(*criteria).order_by(Item.item_id).all()
        session.close()
        return results

    def list_item_types(self, query: ItemTypeQuery) -> List[ItemType]:
        session = self.session_factory()
        criteria = []
        if query.ids:
            criteria.append(ItemType.item_type_id.in_(query.ids))
        if query.text_search:
            criteria.append(ItemType.name.match(query.text_search))

        results = session.query(ItemType).filter(*criteria).order_by(ItemType.producer.asc(), ItemType.name.asc()).all()
        session.close()
        return results

    def list_clients(self, query: ClientQuery) -> List[Client]:
        session = self.session_factory()
        criteria = []
        if query.name:
            criteria.append(func.lower(Client.name) == func.lower(query.name))
        if query.email:
            criteria.append(func.lower(Client.email) == func.lower(query.email))
        if query.ids:
            criteria.append(Client.client_id.in_(query.ids))

        results = session.query(Client).filter(*criteria).order_by(Client.name).all()
        session.close()
        return results

    def list_collections(self, query: CollectionQuery) -> List[ItemCollection]:
        session = self.session_factory()
        criteria = []
        if query.ids:
            criteria.append(ItemCollection.collection_id.in_(query.ids))
        if query.client_ids:
            criteria.append(ItemCollection.client_id.in_(query.client_ids))
        if query.name:
            criteria.append(func.lower(ItemCollection.name) == func.lower(query.name))

        results = session.query(ItemCollection).filter(*criteria).order_by(ItemCollection.name).all()
        session.close()
        return results