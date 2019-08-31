from . import views
from .models import *
from flask import request, url_for, session
from sqlalchemy.exc import IntegrityError
import hashlib
from datetime import datetime,timedelta
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
# 普通页面
###################################################################

# 首页
def index() :
    category_list = Category.query.all()
    recent_articles =Article.query.order_by(Article.date.desc()).limit(20)
    
    article = Article.query.order_by(Article.date.desc()).first()
    
    return views.render_index(site_title(), category_list, recent_articles, article)

# 文章内容
def article_reading() :
    category_list = Category.query.all()
    recent_articles =Article.query.order_by(Article.date.desc()).limit(20)

    article_id = request.args.get('id', 1, type=int)
    article = Article.query.filter_by(id=article_id).first()
    return views.render_article_reading(site_title(), category_list, recent_articles, article)

# 文章列表
def article_list() :
    category_list = Category.query.all()
    recent_articles =Article.query.order_by(Article.date.desc()).limit(20)

    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', None, type=int) 
    category = Category.query.filter_by(id=category_id).first()
    if category_id == None :
        pagination = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=10)
    else :
        pagination = Article.query.filter_by(category_id=category_id).order_by(Article.date.desc()).paginate(page=page, per_page=10)
        pagination.category_id = category_id
        if category != None :
            pagination.category_name = category.name
    
    
    return views.render_article_list(site_title(), category_list, recent_articles, pagination)


# 留言页
def message() :
    category_list = Category.query.all()
    recent_articles =Article.query.order_by(Article.date.desc()).limit(20)

    page = request.args.get('page', 1, type=int)
    pagination = Message.query.order_by(Message.date.desc()).paginate(page=page, per_page=20)


    return views.render_message(site_title(), category_list, recent_articles, pagination)

###################################################################
# 管理页面
###################################################################

#admin欢迎页
def admin_index() :
    if is_login() :
        return views.render_admin_index(site_title())
    else :
        return views.redirect(url_for('/admin/login'))

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
            return views.redirect(url_for('/admin/login'), "失败，用户名或密码错误。")
        else :
            session['id'] = user.id
            session['username'] = username
            session['password'] = password
            return views.redirect(url_for('/admin/'))

# 编辑文章
def edit() :
    if is_login() :
        category_list = Category.query.all()
        article_id = request.args.get('id', None, type=int)
        article = Article.query.filter_by(id=article_id).first()
        return views.render_edit(site_title(), category_list, article)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 管理文章
def article_manage() :
    if is_login() :
        page = request.args.get('page', 1, type=int)
        article_list = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=10)
        return views.render_article_manage(site_title(), article_list)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")
    

# 新建文章
def article_create() :
    if is_login() :
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('type')
        user_id = session.get('id')
        article = Article(title=title, content=content, date=utc_now(), 
                            reading=0, user_id=user_id, category_id=category_id)
        db.session.add(article)
        db.session.commit()
        return views.redirect(url_for('/admin/artilce/manage'))
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

#修改文章
def article_modify() :
    if is_login() :
        article_id = request.args.get('id')
        user_id = session.get('id')
        article = Article.query.filter_by(id=article_id, user_id=user_id).first()

        article.title = request.form.get('title')
        article.content = request.form.get('content')
        article.category_id = request.form.get('type')
        
        db.session.add(article)
        db.session.commit()
        return views.redirect(url_for('/admin/artilce/manage'))
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

#删除文章
def article_delete() :
    if is_login() :
        article_id = request.args.get('id')
        article = Article.query.filter_by(id=article_id).first()
        if article != None :
            db.session.delete(article)
            db.session.commit()
        return views.redirect(url_for('/admin/artilce/manage'))
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")


# 管理分类
def category_manage() :
    if is_login() :
        category_list = Category.query.order_by(Category.id.desc()).all()
        return views.render_category_manage(site_title(), category_list)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 修改分类
def category_modify() :
    if is_login() :
        category_id = request.form.get('category_id', None, int)
        category_name = request.form.get('category_name')
        category = Category.query.filter_by(id=category_id).first()

        if category == None :
            category = Category(id=category_id)
            
        category.name = category_name
        db.session.add(category)
        db.session.commit()

        return views.redirect(url_for('/admin/category/manage'))
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 删除分类
def category_delete() :
    if is_login() :
        category_id = request.args.get('id', None, int)
        category = Category.query.filter_by(id=category_id).first()
        if category != None :
            article_list = Article.query.filter_by(category_id=category_id).all()
            for article in article_list :
                article.category_id = Category.id_of_other
                print(article.category_id)
                db.session.add(article)
                db.session.commit()
            db.session.delete(category)
            db.session.commit()

        return views.redirect(url_for('/admin/category/manage'))
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 管理留言
def message_manage() :
    if is_login() :
        page = request.args.get('page', 1, type=int)
        message_list = Message.query.order_by(Message.date.desc()).paginate(page=page, per_page=30)
        return views.render_message_manage(site_title(), message_list)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 新增留言
def message_create() :
    name = request.form.get('name', '匿名', int)
    email = request.form.get('email', None, int)
    content = request.form.get('content')
    msg = Message(name=name, email=email, content=content, date=utc_now())
    db.session.add(msg)
    db.session.commit()

    return views.redirect(url_for('/message'))
    

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
        admin.title = title
        admin.email = email

    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        return views.render_init_result(False, e.args)
    else:
        return views.render_init_result(True, "管理用户初始化成功！")
    