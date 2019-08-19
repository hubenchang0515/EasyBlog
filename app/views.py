from flask import render_template
from flask_bootstrap import Bootstrap

###################################################################
# 普通页面
###################################################################

# 渲染文章内容页面
def render_article(site_title, article=None) :
    return render_template('index.html',site_title=site_title, article=article)

# 渲染文章列表页面
def render_article_list(site_title, article_list=None) :
    return render_template('article_list.html', site_title=site_title, article_list=article_list)






###################################################################
# 管理页面
###################################################################

#欢迎
def render_admin_index(site_title) :
    return render_template('/admin/index.html', site_title=site_title)

#登录
def render_login(site_title, message=None) :
    return render_template('/admin/login.html', site_title=site_title, message=message)


###################################################################
# ! 以下为初始化页面  
###################################################################

# 初始化页面
def render_init() :
    return render_template('/admin/init.html', site_title="Easy Blog")

# 初始化结果页面
def render_init_result(success, message=None) :
    return render_template('/admin/init_result.html', site_title="Easy Blog", success=success, message=message)