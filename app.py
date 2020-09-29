import os
import shelve
# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)
#app.config["DEBUG"] = True
# Create the API
api = Api(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("AllFillings.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
  return "test"

class GetFilling(Resource):
    def get(self, unique_id):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (unique_id in shelf):
            return {'message': 'Record not found', 'data': {}}, 404

        return {'message': 'Record found', 'data': shelf[unique_id]}, 200
    
api.add_resource(GetFilling, '/filing/<string:unique_id>')
