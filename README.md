# EasyBlog
博客程序，原型探索

### 引用的库
* Markdown渲染([Marked](https://github.com/markedjs/marked))
* 代码块语法高亮([Prism](https://github.com/PrismJS/prism))
* HTML标签过滤([DOMPurify](https://github.com/cure53/DOMPurify))
* LaTeX公式渲染([MathJax](https://github.com/mathjax/MathJax))

# Markdown使用帮助
Markdown是一种轻量级标记语言，它十分易于编辑和阅读，并且可以轻而易举地渲染成HTML。  

# 目录
* [转义字符](#转义字符)
* [标题](#标题)
* [段落](#段落)
* [引用](#引用)
* [强调](#强调)
* [分割线](#分割线)
* [删除线](#删除线)
* [超链接](#超链接)
* [图片](#图片)
* [列表](#列表)
* [表格](#表格)
* [行内代码](#行内代码)
* [多行代码](#多行代码)
* [数学公式](#数学公式)

## 转义字符
Markdown中的一些字符有特殊含义，为了使用该字符本身，需要在其前面加上`\`进行转义。  
>例如：`~`表示~删除线~，而`\~`则表示\~字符本身。  

除此之外，以`$$`开头，并以`$$`结尾的内容，不会被进行任何渲染。

## 标题
Markdown使用连续多个`#`开头的行来表示标题，它用1\~6个`#`分别表示1\~6级标题。
```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```

## 段落
一个空行(即连续两个换行符)表示一个段落的开始或结束，和HTML一样，段落内的所有空白字符均只会表示成一个空格，如果要在段落内强制换行，则需要使用**连续的两个空格加一个换行符**。

## 引用
以连续`>`开头的段落表示引用，`>`的数量表示引用嵌套的层数。
> 引用
>> 二层嵌套  

## 强调
被一对`*`包裹的词会被渲染成\<em\>标签，被一对`**`包裹的词会被渲染成\<strong\>标签。  
* *em通常被渲染成斜体*  
* **strong通常被加粗**

## 分割线  
单独的段落，内容为连续三个以上的`-`或`_`或`*`，并且不含其它字符，可以生成一条分割线。

---

## 删除线
以一对`~~`包裹起来的内容，会被添加上~~删除线~~。

## 超链接
超链接的表示方式为：`[显示的内容](链接的URL)` 。

## 图片
图片的方式为：`![图片标题](图片的URL)`。

## 列表
以`*`开头的行表示列表的一项，可以在开头添加空格来进行嵌套。
```markdown
* 文章
  * 新建文章
  * 修改文章
  * 删除文章
* 留言
  * 新建留言
  * 删除留言
```

## 表格
使用`|`画成表格的样子即可生成表格。
```markdown
| ID | 姓名 | 性别 |
| :-: | :-:| :-: |                （这一行表示对齐方式）
| 1| Tom | 男 |
| 2 | Jerry | 男 |
```

| ID | 姓名 | 性别 |
| :-: | :-:| :-: | 
| 1| Tom | 男 |
| 2 | Jerry | 男 |

## 行内代码
以一对反引号(\`)包裹起来的内容，会被渲染为`行内代码`。

## 多行代码
以连续三个反引号的行开始，以连续三个反引号的行为结束的一块内容，为代码块。
```
```C++                    (代码块开始，可以标明语言从而启用语法高亮)
#include <iostream>
int main()
{
    std::cout << "hello world" << std::endl;
    return 0;
}
```                       (代码块结束)
```
```C++  
#include <iostream>
int main()
{
    std::cout << "hello world" << std::endl;
    return 0;
}
```

## 数学公式
使用一对`$$`包裹起来的内容不会被Markdown渲染，在其中写入LaTex可以被MathJax渲染成数学公式。
```
$$
S(r_k)  = \sum_{r_k \ne r_i} \text{exp}(\frac{-D_s(r_k, r_i)}{\sigma_s^2})
\tag{1}
$$
```
$$
S(r_k)  = \sum_{r_k \ne r_i} \text{exp}(\frac{-D_s(r_k, r_i)}{\sigma_s^2})
\tag{1}
$$
