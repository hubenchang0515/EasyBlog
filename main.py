from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import timedelta
from app import init
from app.models import create_database, init_database
import app.controllers 

routes = [
    ###################################################################
    # 普通页面
    ###################################################################
    ['/',                   app.controllers.index],
    ['/article/list',       app.controllers.article_list],


    ###################################################################
    # 管理页面
    ###################################################################
    ['/admin/',                 app.controllers.admin_index],
    ['/admin/login',            app.controllers.login],
    ['/admin/article/edit',     app.controllers.edit],
    ['/admin/article/create',   app.controllers.article_create],
    ['/admin/article/manage',   app.controllers.article_manage],
    ['/admin/article/modify',   app.controllers.article_modify],
    ['/admin/article/delete',   app.controllers.article_delete],
    
]

if __name__ == "__main__":
    app = init()
    create_database(app)
    init_database(app)

    for route in routes :
        app.add_url_rule(route[0], endpoint=route[0], view_func=route[1], methods=['GET','POST'])

    app.run(port=80, debug=True)