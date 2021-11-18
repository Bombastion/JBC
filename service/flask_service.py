import logging

from flask import Flask, json, render_template, request
from werkzeug.exceptions import HTTPException, BadRequest

from db.model.client import Client
from db.model.item_type import ItemType
from db.model.model_handler import ClientQuery, ItemTypeQuery, ModelHandler
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

   return new_type.item_type_id

@app.route('/add_new_client', methods=['POST'])
def add_new_client():
   handler = ModelHandler(SessionFactory)
   name, email = request.form['new_client_name'], request.form['new_client_email']
   existing_clients = handler.list_clients(ClientQuery(email=email))
   if len(existing_clients) > 0:
      raise InvalidArgument(f"Client with the provided email {email} already exists with ID {existing_clients[0].client_id}!")
   new_client = Client(name=name, email=email)
   handler.persist_object(new_client)

   return new_client.client_id

@app.route('/get_item_types', methods=['GET'])
def get_item_types():
   handler = ModelHandler(SessionFactory)
   query = ItemTypeQuery()
   item_types = handler.list_item_types(query)
   return render_template('type_list.html', item_types=item_types)


if __name__ == '__main__':
   logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', level=logging.DEBUG, )
   app.run(host="0.0.0.0")
