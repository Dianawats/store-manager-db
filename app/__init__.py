#imported flask
from flask import Flask
#create an object of flask using a unique name
app = Flask(__name__)
#import the views for the routes of the app
from app import views