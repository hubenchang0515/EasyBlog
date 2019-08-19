from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import timedelta
from app import init
from app.models import create_database, init_database
import app.controllers 

routes = [
    ['/',                   app.controllers.index],
    ['/article_list',       app.controllers.article_list]
]

if __name__ == "__main__":
    app = init()
    create_database(app)
    init_database(app)

    for route in routes :
        app.add_url_rule(route[0], endpoint=route[0], view_func=route[1], methods=['GET','POST'])

    app.run(port=80, debug=True)