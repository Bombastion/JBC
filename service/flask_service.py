from flask import Flask, render_template, request
import logging
from db.model.item_type import ItemType

from db.model.model_handler import ItemTypeQuery, ModelHandler
from db.model.sqlalchemy_base import SessionFactory

app = Flask(__name__)

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

@app.route('/get_item_types', methods=['GET'])
def get_item_types():
   handler = ModelHandler(SessionFactory)
   query = ItemTypeQuery()
   item_types = handler.list_item_types(query)
   return render_template('type_list.html', item_types=item_types)


if __name__ == '__main__':
   logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', level=logging.DEBUG, )
   app.run(host="0.0.0.0")
