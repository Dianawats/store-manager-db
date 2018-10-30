#imported flask
from flask import Flask
#create an object of flask using a unique name
app = Flask(__name__)

from app.authentication.authenticate import auth_blueprint
from app.views import views_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(views_blueprint)

app.config['JWT_SECRET_KEY'] = '0ct0p1330'
from flask_jwt_extended import JWTManager
jwt = JWTManager(app)
