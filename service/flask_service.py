from flask import Flask
import logging

import db.model

app = Flask(__name__)

@app.route('/')
def hello_world():
   return """
      _<br/> 
     / \\<br/>
    /   \\<br/>
   (_____)
   """

if __name__ == '__main__':
   app.run()