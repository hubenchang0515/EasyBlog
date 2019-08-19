from . import views
from .models import *
from flask import request 
from sqlalchemy.exc import IntegrityError
import hashlib

# 加密
def encrypt(salt, data) :
    encryptor = hashlib.sha256(salt.encode("utf-8"))
    encryptor.update(data.encode("utf-8"))
    return encryptor.hexdigest()

# 首页
def index() :
    article = Article.query.order_by(Article.date.desc()).first()
    return views.render_article(article)

# 文章列表
def article_list() :
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=10)
    return views.render_article_list(pagination)


###################################################################
# ! 以下为初始化页面  
###################################################################
def init() :
    return views.render_init()

def init_result() :
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password-again')
    email = request.form.get('e-mail')

    if password != password2 :
        return views.render_init_result(False, "两次输入的密码不同！")

    password = encrypt(username, password)

    admin = User.query.filter_by(role_id=Role.id_of_admin).first()
    if admin == None :
        admin = User(id=User.id_of_admin, role_id=Role.id_of_admin, username=username, password=password, email=email)
    else :
        admin.username = username
        admin.password = password
        admin.email = email

    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        return views.render_init_result(False, e.args)
    else:
        return views.render_init_result(True, "管理用户初始化成功！")
    