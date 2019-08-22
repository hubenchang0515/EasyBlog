from . import views
from .models import *
from flask import request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError
import hashlib
from datetime import datetime
import pytz

###################################################################
# 辅助函数
###################################################################

# 加密
def encrypt(salt, data) :
    encryptor = hashlib.sha256(salt.encode("utf-8"))
    encryptor.update(data.encode("utf-8"))
    return encryptor.hexdigest()

# 当前UTC时间
def utc_now() :
    utc_tz = pytz.timezone('UTC')
    return datetime.now(tz=utc_tz)

# 站点标题
def site_title() :
    user = User.query.filter_by(id=User.id_of_admin).first()
    if user == None :
        return "Easy Blog"
    else :
        return user.title

###################################################################
# 普通页面
###################################################################

# 首页
def index() :
    article = Article.query.order_by(Article.date.desc()).first()
    return views.render_article(site_title(), article)

# 文章列表
def article_list() :
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=10)
    return views.render_article_list(site_title(), pagination)

# 检测session，判断是否登录
def is_login() :
    username = session.get('username')
    password = session.get('password')
    user = User.query.filter_by(id=User.id_of_admin, username=username, password=password).first()
    if user == None :
        return False
    else :
        return True


###################################################################
# 管理页面
###################################################################

#admin欢迎页
def admin_index() :
    if is_login() :
        return views.render_admin_index(site_title())
    else :
        return redirect(url_for('/admin/login'))

# 登录
def login() :
    username = request.form.get('username')
    password = request.form.get('password')
    if username == None and password == None :
        return views.render_login(site_title())
    else :
        password = encrypt(username, password)
        user = User.query.filter_by(id=User.id_of_admin, username=username, password=password).first()
        if user == None :
            return views.render_login(site_title(), "用户名或密码错误。")
        else :
            session['id'] = user.id
            session['username'] = username
            session['password'] = password
            return redirect(url_for('/admin/'))

# 新建文章
def article_create() :
    if is_login() :
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('id')
        article = Article(title=title, content=content, date=utc_now(), 
                            reading=0, user_id=user_id, category_id=Category.id_of_other)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('/admin/'))
    else :
        return redirect(url_for('/admin/login'))

# 编辑文章
def edit() :
    if is_login() :
        typelist = Category.query.all()
        return views.render_edit(site_title(), typelist)
    else :
        return redirect(url_for('/admin/login'))

###################################################################
# ! 以下为初始化页面  
###################################################################
def init() :
    return views.render_init()

def init_result() :
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password-again')
    title = request.form.get('site')
    email = request.form.get('e-mail')

    if password != password2 :
        return views.render_init_result(False, "两次输入的密码不同！")

    password = encrypt(username, password)

    admin = User.query.filter_by(role_id=Role.id_of_admin).first()
    if admin == None :
        admin = User(id=User.id_of_admin, role_id=Role.id_of_admin, username=username, password=password,title=title, email=email)
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
    