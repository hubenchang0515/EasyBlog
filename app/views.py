from flask import render_template
from flask_bootstrap import Bootstrap

###################################################################
# 跳转
###################################################################
def redirect(url, alert=None) :
    return render_template("redirect.html", alert=alert, url=url)


###################################################################
# 普通页面
###################################################################

# 渲染文章内容页面
def render_index(site_title, category_list, recent_articles, article=None) :
    return render_template('public.html',site_title=site_title, category_list=category_list, recent_articles=recent_articles, article=article)

def render_article_reading(site_title, category_list, recent_articles, article=None, comment_list=None) :
    return render_template('/article/reading.html',site_title=site_title, category_list=category_list, recent_articles=recent_articles, article=article, comment_list=comment_list)

# 渲染文章列表页面
def render_article_list(site_title, category_list, recent_articles, article_list=None) :
    return render_template('/article/list.html', site_title=site_title, category_list=category_list, recent_articles=recent_articles, article_list=article_list)

# 渲染留言页面
def render_message(site_title, category_list, recent_articles, message_list=None) :
    return render_template('/message.html', site_title=site_title, category_list=category_list, recent_articles=recent_articles, message_list=message_list)




###################################################################
# 管理页面
###################################################################

# 欢迎
def render_admin_index(site_title) :
    return render_template('/admin/index.html', site_title=site_title)

# 登录
def render_login(site_title, message=None) :
    return render_template('/admin/login.html', site_title=site_title, message=message)

# 编辑文章
def render_edit(site_title, category_list, article=None) :
    return render_template('/admin/article/edit.html', site_title=site_title, category_list=category_list, article=article)

# 管理文章
def render_article_manage(site_title, article_list=None) :
    return render_template('/admin/article/manage.html', site_title=site_title, article_list=article_list)

# 管理分类
def render_category_manage(site_title, category_list=None) :
    return render_template('/admin/category/manage.html', site_title=site_title, category_list=category_list)

# 管理留言
def render_message_manage(site_title, message_list=None) :
    return render_template('/admin/message/manage.html', site_title=site_title, message_list=message_list)

###################################################################
# ! 以下为初始化页面  
###################################################################

# 初始化页面
def render_init() :
    return render_template('/admin/init/init.html', site_title="Easy Blog")

# 初始化结果页面
def render_init_result(success, message=None) :
    return render_template('/admin/init/init_result.html', site_title="Easy Blog", success=success, message=message)