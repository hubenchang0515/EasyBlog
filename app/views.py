from flask import render_template
from flask_bootstrap import Bootstrap

# 渲染文章内容页面
def render_article(article=None) :
    return render_template('index.html', article=article)

# 渲染文章列表页面
def render_article_list(article_list) :
    return render_template('article_list.html', article_list=article_list)


###################################################################
# ! 以下为初始化页面  
###################################################################

# 初始化页面
def render_init() :
    return render_template('init.html')

# 初始化结果页面
def render_init_result(success, message) :
    return render_template('init_result.html', success=success, message=message)