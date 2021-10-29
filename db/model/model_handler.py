from typing import Any

from db.model import Client, Item, ItemCollection, ItemType

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