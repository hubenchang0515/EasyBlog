from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import timedelta
from app import init
from app.models import create_database, init_database
import app.controllers 

routes = [
    ['/',                   app.controllers.init],
    ['/init_result',        app.controllers.init_result]
]


if __name__ == "__main__":
    app = init()
    create_database(app)
    init_database(app)

    for route in routes :
        app.add_url_rule(route[0], endpoint=route[0], view_func=route[1], methods=['GET','POST'])

    @app.route('/<other>')
    def other_url(other) :
        return "<h1>请切换到 80 端口，并关闭 admin.py 进程。</h1>"

    app.run(host="0.0.0.0", port=23646, debug=True)