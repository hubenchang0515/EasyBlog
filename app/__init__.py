import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

bootstrap = Bootstrap()
alchemy = SQLAlchemy()
moment = Moment()

def init() :
    app = Flask(__name__)

    sql_url = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "database.sqlite")
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_url
    #app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = os.urandom(64)

    bootstrap.init_app(app)
    alchemy.init_app(app)
    moment.init_app(app)

    return app