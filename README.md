# EasyBlog
博客程序，原型探索

## 引用源码
* Markdown渲染([Marked](https://github.com/markedjs/marked))
* 代码块语法高亮([Prism](https://github.com/PrismJS/prism))
* HTML过滤([DOMPurify](https://github.com/cure53/DOMPurify))
* LaTeX公式渲染([MathJax](https://github.com/mathjax/MathJax))

## 部署
1. 安装依赖。
```
pip install -r requirements.txt
```
2. 运行 `admin.py` 登录 `23646` 进行初始化(配置用户名及密码)，初始化完成后**关闭此进程**。
3. 运行 `main.py` 登录 `80` 端口即可使用。

> 程序当前设置为`DEBUG`模式，可以自行更改及配置`uWSGI`。

## 预览
![reading](https://github.com/hubenchang0515/resource/blob/master/easy-blog/reading.png?raw=true)

![reading](https://github.com/hubenchang0515/resource/blob/master/easy-blog/edit.png?raw=true)

![reading](https://github.com/hubenchang0515/resource/blob/master/easy-blog/message.png?raw=true)

![reading](https://github.com/hubenchang0515/resource/blob/master/easy-blog/category-manage.png?raw=true)