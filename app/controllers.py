from . import views
from .models import *
from flask import request, url_for, session
import hashlib
from datetime import datetime, timedelta
import pytz
import random

###################################################################
# 留言和回复为空时，随机生成一条
###################################################################
def random_message():
    # 使用东八区的时间
    today = datetime.utcnow()
    today = today + timedelta(hours=8)

    if today.month == 1 and today.day == 1 :
        return "新年快乐，万事如意！"

    if today.month == 5 and today.day == 1:
        return "全世界无产阶级联合起来"

    if today.month == 5 and today.day == 12:
        return "向全体南丁格尔小姐致以节日的祝贺和崇高敬意"

    if today.month == 5 and today.day == 15:
        return "生日快乐"

    if today.month == 6 and today.day == 1:
        return "儿童节快乐"

    if today.month == 7 and today.day == 7:
        return "庆祝中国人民抗日战争胜利%d周年" % (today.year - 1945)

    if today.month == 10 and today.day == 1:
        return "庆祝中华人民共和国成立%d周年" % (today.year - 1949)


    if today.month == 12 and today.day in (24, 25):
        return "🎄Merry Christmas"

    message_list = [
        "好！顶！赞！", 

        "富强 民主 文明 和谐 自由 平等 公正 法治 爱国 敬业 诚信 友善",

        "我有一头小毛驴，我从来也不骑。",

        "在山的那边，海的那边，有一群蓝精灵。",

        "爆ぜろリアル  弾けろシナプス   バニッシュメント・ディス・ワールド！",

        "今天的风儿甚为喧嚣呢。"
    ]

    return random.choice(message_list)

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
    if article != None :
        article.reading += 1
        db.session.add(article)
        db.session.commit()

    page = request.args.get('page', 1, type=int)
    comment_list = Comment.query.filter_by(article_id=article_id).order_by(Comment.date.desc()).paginate(page=page, per_page=10)

    return views.render_article_reading(site_title(), category_list, recent_articles, article, comment_list)

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
        return views.redirect(url_for('/admin/article/manage'))
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
        return views.redirect(url_for('/admin/article/manage'))
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
        return views.redirect(url_for('/admin/article/manage'))
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
    email = request.form.get('email', None, str)
    content = request.form.get('content', None, str)
    if content is None or len(content.strip()) == 0:
        content = random_message()

    msg = Message(name=name, email=email, content=content, date=utc_now())
    db.session.add(msg)
    db.session.commit()

    return views.redirect(url_for('/message'))
    

# 删除留言
def message_delete() :
    if is_login() :
        id = request.args.get('id',type=int)
        msg = Message.query.filter_by(id=id).first()
        if msg != None :
            db.session.delete(msg)
            db.session.commit()
            return views.redirect(url_for('/admin/message/manage'))
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 管理回复
def comment_manage() :
    if is_login() :
        page = request.args.get('page', 1, type=int)
        comment_list = Comment.query.order_by(Comment.date.desc()).paginate(page=page, per_page=30)
        return views.render_comment_manage(site_title(), comment_list)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")
    
    
# 新增回复
def comment_create() :
    name = request.form.get('name', '匿名', int)
    email = request.form.get('email', None, str)
    article_id = request.args.get('article_id', type=int)
    content = request.form.get('content', None, str)
    if content is None or len(content.strip()) == 0:
        content = random_message()
    comment = Comment(name=name, email=email, content=content, date=utc_now(), article_id=article_id)
    db.session.add(comment)
    db.session.commit()
    url_to = "/article/reading?id=" + str(article_id)
    return views.redirect(url_to)

# 删除回复
def comment_delete() :
    if is_login() :
        id = request.args.get('id',type=int)
        page = request.args.get('page', type=int, default=1)
        comment = Comment.query.filter_by(id=id).first()
        if comment != None :
            db.session.delete(comment)
            db.session.commit()

        url = '/admin/comment/manage?page=' + str(page)
        return views.redirect(url)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 设置页面
def config() :
    if is_login() :
        id = session.get('id')
        cfg = User.query.filter_by(id=id).first()
        if(cfg != None) :
            return views.render_config(site_title(), cfg)
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 修改密码
def config_password() :
    if is_login() :
        id = session.get('id')
        username = session.get('username')
        cfg = User.query.filter_by(id=id).first()
        if(cfg != None) :
            cfg.password = encrypt(username, request.form.get('password'))
            db.session.add(cfg)
            db.session.commit()
            return views.redirect(url_for('/admin/config'), "密码修改成功。")
        else :
            return views.redirect(url_for('/admin/login'), "登录超时。")
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 修改站点标题
def config_title() :
    if is_login() :
        id = session.get('id')
        cfg = User.query.filter_by(id=id).first()
        if(cfg != None) :
            cfg.title = request.form.get('title')
            db.session.add(cfg)
            db.session.commit()
            return views.redirect(url_for('/admin/config'), "站点标题修改成功。")
        else :
            return views.redirect(url_for('/admin/login'), "登录超时。")
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 修改邮箱地址
def config_email() :
    if is_login() :
        id = session.get('id')
        cfg = User.query.filter_by(id=id).first()
        if(cfg != None) :
            cfg.email = request.form.get('email')
            db.session.add(cfg)
            db.session.commit()
            return views.redirect(url_for('/admin/config'), "邮箱地址修改成功。")
        else :
            return views.redirect(url_for('/admin/login'), "登录超时。")
    else :
        return views.redirect(url_for('/admin/login'), "请登录。")

# 退出登录
def logout() :
    session.pop('id')
    session.pop('username')
    session.pop('password')
    return views.redirect(url_for('/admin/login'), "已退出。")


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
    