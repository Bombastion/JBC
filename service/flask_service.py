import logging

from flask import Flask, json, jsonify, render_template, request
from werkzeug.exceptions import HTTPException, BadRequest
from db.model import client

from db.model.client import Client
from db.model.item_collection import ItemCollection
from db.model.item_type import ItemType
from db.model.model_handler import ClientQuery, CollectionQuery, ItemTypeQuery, ModelHandler
from db.model.sqlalchemy_base import SessionFactory
from service.exception import(
   InvalidArgument,
)

app = Flask(__name__)

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/')
def landing_page():
   return render_template('index.html')


@app.route('/add_new_item_type', methods=['POST'])
def add_new_item_type():
   handler = ModelHandler(SessionFactory)
   name, producer = request.form['new_item_type_name'], request.form['new_item_type_producer']
   new_type = ItemType(name=name, producer=producer)
   handler.persist_object(new_type)

   return new_type.to_dict()

@app.route('/add_new_client', methods=['POST'])
def add_new_client():
   handler = ModelHandler(SessionFactory)
   name, email = request.form['new_client_name'], request.form['new_client_email']
   existing_clients = handler.list_clients(ClientQuery(email=email))
   if len(existing_clients) > 0:
      raise InvalidArgument(f"Client with the provided email {email} already exists with ID {existing_clients[0].client_id}!")
   new_client = Client(name=name, email=email)
   handler.persist_object(new_client)

   return new_client.to_dict()

@app.route('/add_new_collection', methods=['POST'])
def add_new_collection():
   handler = ModelHandler(SessionFactory)
   name, client_id = request.form['new_collection_name'], request.form['client_id']
   existing_collections = handler.list_collections(CollectionQuery(client_ids=[client_id], name=name))
   if len(existing_collections) > 0:
      raise InvalidArgument(f"Collection with name {existing_collections[0].name} already exists for client ID {client_id} with ID {existing_collections[0].collection_id}!")
   new_collection = ItemCollection(name=name, client_id=client_id)
   handler.persist_object(new_collection)

   return new_collection.to_dict()

@app.route('/get_item_types', methods=['GET'])
def get_item_types():
   handler = ModelHandler(SessionFactory)
   query = ItemTypeQuery()
   item_types = handler.list_item_types(query)
   return jsonify(
      item_types=[item_type.to_dict() for item_type in item_types],
   )

@app.route('/get_collections', methods=['GET'])
def get_collections():
   client_id = request.form.get('client_id', None)
   collection_id = request.form.get('collection_id', None)

   handler = ModelHandler(SessionFactory)
   query = CollectionQuery()
   if collection_id:
      query.ids = [collection_id]
   if client_id:
      query.client_ids = [client_id]

   matching_collections = handler.list_collections(query)

   return jsonify(
      collections=[collection.to_dict() for collection in matching_collections],
   )

if __name__ == '__main__':
   logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', level=logging.DEBUG, )
   app.run(host="0.0.0.0")
