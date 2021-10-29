from db.model.sqlalchemy_base import SessionFactory
from db.model import Client, ItemType, ItemCollection, Item
from db.model.model_handler import ModelHandler

if __name__ == "__main__":
    handler = ModelHandler(session_factory=SessionFactory)

    sample_client = Client(name='sample', email='example')
    handler.persist_object(sample_client)
    print(sample_client)

    sample_collection = ItemCollection(client_id=sample_client.client_id, name="test collection")
    handler.persist_object(sample_collection)
    print(sample_collection)

    sample_type = ItemType(name="sample")
    handler.persist_object(sample_type)
    print(sample_type)

    # Due to FK constraints, order matters here
    handler.delete_object(sample_collection)
    handler.delete_object(sample_type)
    handler.delete_object(sample_client)
