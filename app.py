import os
import shelve
# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)
app.config["DEBUG"] = True
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

class Create(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unique_id', required=True)
        parser.add_argument('link')
        parser.add_argument('user')
        parser.add_argument('stockCodes')
        parser.add_argument('row_id')
        parser.add_argument('order_id')
        parser.add_argument('created_date')
        # Parse the arguments into an object
        args = parser.parse_args()
        shelf = get_db()
        shelf[args['unique_id']] = args

        return {'message': 'Record Created', 'data': args}, 201 

class AllFilingList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200

api.add_resource(Create, '/createfilling')  
api.add_resource(GetFilling, '/filing/<string:unique_id>')
api.add_resource(AllFilingList, '/allfiling')
app.run()