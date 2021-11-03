from flask import Flask, render_template
import logging

import db.model

app = Flask(__name__)

@app.route('/')
def landing_page():
   return render_template('index.html', name="Fish")


if __name__ == '__main__':
   app.run(host="0.0.0.0")