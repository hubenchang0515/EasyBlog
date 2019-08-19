from flask_sqlalchemy import SQLAlchemy
from . import alchemy as db

# 用户角色
class Role(db.Model) :
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')

    id_of_admin = 1

    def __repr__(self) :
        return '<Role %r>' % self.name


# 用户
class User(db.Model) :
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    articles = db.relationship('Article', backref='user')

    id_of_admin = 1

    def __repr__(self) :
        return '<Role %r>' % self.username

# 文章分类
class Category(db.Model) :
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    articles = db.relationship('Article', backref='category')

    id_of_other = 1

    def __repr__(self) :
        return '<Category %r>' % self.name

# 文章
class Article(db.Model) :
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False) # 以时间戳的形式保存
    reading = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'), nullable=False)

    comments = db.relationship('Comment', backref='article')

    def __repr__(self) :
        return '<Article %r>' % self.title

# 文章评论
class Comment(db.Model) :
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    content = db.Column(db.String(2048), nullable=False)
    date = db.Column(db.Date, nullable=False) # 以时间戳的形式保存

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)

    def __repr__(self) :
        return '<Comment %r>' % self.id

# 留言
class Message(db.Model) :
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    content = db.Column(db.String(2048), nullable=False)
    date = db.Column(db.Date, nullable=False) # 以时间戳的形式保存

    def __repr__(self) :
        return '<Comment %r>' % self.id


# 创建数据库
def create_database(app) :
    with app.app_context():
        db.create_all()

# 初始化数据库
def init_database(app) :
    with app.app_context():
        if Role.query.filter_by(id=1).first() == None :
            admin = Role(id=Role.id_of_admin, name="admin")
            db.session.add(admin)
            db.session.commit()

        if Category.query.filter_by(id=1).first() == None :
            other = Category(id=Category.id_of_other, name="未分类")
            db.session.add(other)
            db.session.commit()