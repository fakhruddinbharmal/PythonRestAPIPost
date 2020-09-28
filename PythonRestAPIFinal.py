#import markdown
import os
import shelve

# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
app = Api(app)
app.config["DEBUG"] = True

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

@app.route('/',methods=['POST'])
def post():
    parser = reqparse.RequestParser()
    parser.add_argument('unique_id', required=True)
    parser.add_argument('link')
    parser.add_argument('user')
    parser.add_argument('stockCodes')
    parser.add_argument('row_id')
    parser.add_argument('order_id')
    parser.add_argument('created_date')
    #Parse the arguments into an object
    args = parser.parse_args()
    shelf = get_db()
    shelf[args['unique_id']] = args

    return {'message': 'Record Created', 'data': args}, 201
app.run(port=5002)