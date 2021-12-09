import logging
import traceback
import uuid

from flask import flash, Flask, json, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException, BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from db.model.client import Client
from db.model.item import Item
from db.model.item_collection import ItemCollection
from db.model.item_type import ItemType
from db.model.model_handler import ClientQuery, CollectionQuery, ItemQuery, ItemTypeQuery, ModelHandler
from db.model.sqlalchemy_base import SessionFactory

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.login_view = 'login_wrapper'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
   handler = ModelHandler(SessionFactory)
   existing_clients = handler.list_clients(ClientQuery(ids=[user_id]))
   if len(existing_clients) != 1:
      raise ValueError(f"Found more than one user for ID {user_id}")
   return existing_clients[0]

def hash_password(plaintext: str) -> str:
   return generate_password_hash(plaintext, method='sha256')

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


def entry_exit_logging(func):
   """
   Simple error handler that logs errors
   """
   def inner_func(*args, **kwargs):
      request_id = uuid.uuid4()
      try:
         # Log common info about the request
         logging.info(f"[{request_id}] Entering {func.__name__}")
         request_form_dict = dict(request.form)
         # Don't log passwords in plain text
         if request_form_dict.get("password", None):
            request_form_dict["password"] = "..."
         logging.info(f"[{request_id}] Request form: {request_form_dict}")
         logging.info(f"[{request_id}] Request args: {request.args}")

         result = func(*args, **kwargs)

         # Log common exit info and return
         logging.info(f"[{request_id}] Exiting {func.__name__}")
         return result
      except Exception as e:
         logging.error(f"[{request_id}] Encountered error in {func.__name__}")
         logging.error(f"[{request_id}] {traceback.format_exc()}")
         # Add more specific handling as needed here
         if isinstance(e, ValueError):
            raise BadRequest(f"[{request_id}] {str(e)}")
   inner_func.__name__ = f"{func.__name__}_wrapper"
   return inner_func

@app.route('/')
@entry_exit_logging
def landing_page():
   return render_template('index.html')

@app.route('/authExample')
@entry_exit_logging
def auth_base():
   return render_template('base.html')

@app.route('/login', methods=['GET'])
@entry_exit_logging
def login():
   return render_template('login.html')

@app.route('/login', methods=['POST'])
@entry_exit_logging
def login_post():
   email = request.form.get('email')
   password = request.form.get('password')
   remember = True if request.form.get('remember') else False

   handler = ModelHandler(SessionFactory)
   existing_clients = handler.list_clients(ClientQuery(email=email))

   if len(existing_clients) > 1:
      raise ValueError(f"Provided email {email} has more than one user associated with it. Please contact admin support")

   if len(existing_clients) < 1 or not check_password_hash(existing_clients[0].password, password):
      flash("[danger]Email or password doesn't match. Please try again")
      return redirect(url_for('login_wrapper'))

   login_user(existing_clients[0], remember=remember)
   return redirect(url_for('user_cellars_page_wrapper'))

@app.route('/logout')
@login_required
@entry_exit_logging
def logout():
   logout_user()
   return redirect(url_for('login_wrapper'))

@app.route('/signup', methods=['GET'])
@entry_exit_logging
def signup():
   return render_template('signup.html')

@app.route('/signup', methods=["POST"])
@entry_exit_logging
def signup_post():
   email = request.form.get('email')
   name = request.form.get('name')
   password = request.form.get('password')

   handler = ModelHandler(SessionFactory)
   existing_clients = handler.list_clients(ClientQuery(email=email))

   if len(existing_clients) > 0: # if a user is found, we want to redirect back to signup page so user can try again
      flash("[danger]A user with that email already exists")
      return redirect(url_for('signup_wrapper'))

   # create a new user with the form data. Hash the password so the plaintext version isn't saved.
   new_client = Client(email=email, name=name, password=hash_password(password))

   # add the new user to the database
   handler.persist_object(new_client)

   flash("[success]Signup successful! Please log in with your new account")
   return redirect(url_for('login_wrapper'))

@app.route('/myCellars')
@login_required
@entry_exit_logging
def user_cellars_page():
   return render_template('user_collections.html')

@app.route('/add_new_item_type', methods=['POST'])
@entry_exit_logging
def add_new_item_type():
   name, producer = request.form['new_item_type_name'], request.form['new_item_type_producer']
   handler = ModelHandler(SessionFactory)
   new_type = ItemType(name=name, producer=producer)
   handler.persist_object(new_type)

   return new_type.to_dict()

@app.route('/add_new_client', methods=['POST'])
@entry_exit_logging
def add_new_client():
   handler = ModelHandler(SessionFactory)
   name, email, password = request.form['new_client_name'], request.form['new_client_email'], request.form['new_client_password']
   existing_clients = handler.list_clients(ClientQuery(email=email))
   if len(existing_clients) > 0:
      raise ValueError(f"Client with the provided email {email} already exists with ID {existing_clients[0].client_id}!")
   new_client = Client(name=name, email=email, password=password)
   handler.persist_object(new_client)

   return new_client.to_dict()


@app.route('/add_new_collection', methods=['POST'])
@entry_exit_logging
def add_new_collection():
   handler = ModelHandler(SessionFactory)
   name, client_id = request.form['new_collection_name'], request.form['client_id']
   existing_collections = handler.list_collections(CollectionQuery(client_ids=[client_id], name=name))
   if len(existing_collections) > 0:
      raise ValueError(f"Collection with name {existing_collections[0].name} already exists for client ID {client_id} with ID {existing_collections[0].collection_id}!")
   new_collection = ItemCollection(name=name, client_id=client_id)
   handler.persist_object(new_collection)

   return new_collection.to_dict()

@app.route('/get_items', methods=['GET'])
@entry_exit_logging
def get_items():
   collection_id = request.args.get('collection_id', None)

   handler = ModelHandler(SessionFactory)
   query = ItemQuery()
   query.collection_ids = [collection_id]

   items = handler.list_items(query)
   return jsonify(
      items=[item.to_dict() for item in items],
   )

@app.route('/get_item_types', methods=['GET'])
@entry_exit_logging
def get_item_types():
   handler = ModelHandler(SessionFactory)
   query = ItemTypeQuery()
   item_type_id = request.args.get('item_type_id', None)
   if item_type_id:
      query.ids = [item_type_id]

   item_types = handler.list_item_types(query)
   return jsonify(
      item_types=[item_type.to_dict() for item_type in item_types],
   )

@app.route('/get_collections', methods=['GET'])
@entry_exit_logging
def get_collections():
   client_id = request.args.get('client_id', None)
   collection_id = request.args.get('collection_id', None)

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

@app.route('/add_item_to_collection', methods=['POST'])
@entry_exit_logging
def add_item_to_collection():
   collection_id = request.form['collection_id']
   quantity = int(request.form['quantity'])

   if quantity < 1:
      raise ValueError("quantity must be at least 1")
   
   item_type_id = request.form.get('item_type_id', None)

   handler = ModelHandler(SessionFactory)   
   query = ItemQuery(item_type_ids=[item_type_id], collection_ids=[collection_id])
   items = handler.list_items(query)
   if len(items) > 1:
      raise ValueError(f"Found more than one item for item_type_id {item_type_id} in collection {collection_id}")

   item_to_modify = None
   if len(items) == 1:
      item_to_modify = items[0]
      item_to_modify.quantity += quantity
   else: 
      item_to_modify = Item(collection_id=collection_id, quantity=quantity, item_type_id=item_type_id)
   handler.persist_object(item_to_modify)

   return item_to_modify.to_dict()

@app.route('/modify_item', methods=['POST'])
@entry_exit_logging
def modify_item():
   new_quantity = int(request.form['new_quantity'])
   if new_quantity < 0:
      raise ValueError("quantity must be at least 0")
   item_id = request.form['item_id']

   handler = ModelHandler(SessionFactory)   
   query = ItemQuery(ids=[item_id])
   items = handler.list_items(query)
   if len(items) != 1:
      raise ValueError(f"Found more than one item for id {item_id}")

   item_to_modify = items[0]
   item_to_modify.quantity = new_quantity
   if new_quantity == 0:
      handler.delete_object(item_to_modify)
   else:
      item_to_modify.quantity = new_quantity
      handler.persist_object(item_to_modify)

   return item_to_modify.to_dict()

if __name__ == '__main__':
   logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', level=logging.DEBUG, )
   app.run(host="0.0.0.0")
