#import markdown
import os

# Import the framework
from flask import Flask, g
#from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
#api = Api(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/',methods=['get'])
return "hello"
app.run
