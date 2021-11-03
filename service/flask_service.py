from flask import Flask, render_template
import logging
from db.model import item_type

from db.model.model_handler import ItemTypeQuery, ModelHandler
from db.model.sqlalchemy_base import SessionFactory

app = Flask(__name__)

@app.route('/')
def landing_page():
   handler = ModelHandler(SessionFactory)
   query = ItemTypeQuery()
   item_types = handler.list_item_types(query)
   return render_template('index.html', item_types=item_types)


if __name__ == '__main__':
   formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
   logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', level=logging.DEBUG, )
   app.run(host="0.0.0.0")