
## lru_cache
shadowsocks-python版本中LRUCache的复制。

## PTCheck.py
筛选PT上三个热门板块最近两天内豆瓣评分>7.0的影片，发送到我邮箱。

## autoSign
[穿越时空](http://www.go-out.cc)自动签到脚本

## markdown_editor
markdown编辑器web端。 [Demo](http://138.68.18.245:9876/)

1. 支持存档；
2. 可以选择同步到印象笔记（目前只是沙箱环境）可以选择同步到印象笔记（目前只是沙箱环境）；

requirements:
- tornado
- markdown

TODO：
- 有稳定服务器后，激活API key，与真正印象笔记同步；
- 样式；
- 完善异常处理；

## A chatdemo simplified from tornado chatdemo
目前看起来works well。

*但是有一个问题：poll的方式改成GET后，会发生不可思议的问题，改回POST就OK。* 可能理解仍不够深刻。需要多看些处理long poll的代码。

## 知乎爬虫
爬某个用户(user)的所有回答，写入./(user)/文件夹下。

Update:
我写这个爬虫的时候，知乎用户答案的浏览方式是页面拉到底端后加载（和网页版ins相同），然而今天发现浏览方式变成了分页+页面下拉后加载完此页内容。于是修改了下代码。
`do_spider_by_page()`是支持目前浏览方式的爬虫函数，主函数里运行的是这个方法。

Usage:
- `executable_path=r'E:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe'`windows下替换为phantojs.exe的路径，Linux下这个留空即可。
- zhihu_config.ini文件中对应cookie填好。
- `do_spider(username)`中的username填写被爬知乎用户的ID。
- *注意下爬取的时间间隔*，1.4s的时间间隔似乎是可接受的。（至少对800多个答案而言）
- 执行`python zhihu_spider.py`，将在zhihu_spider目录下创建以该用户ID为名的文件夹，用浏览器打开里面的index.html即可。

[Demo](http://138.68.18.245:9888/spiderdemo)
这个demo里面没加样式，实际爬下来之后会有样式，看起来很友好。

requirements:
- selenium
- reqeusts(推荐2.10.0版本，2.12版本会有X509的报错)
- [PhantomJS](http://phantomjs.org/)
- bs4。*selenium应该也能解析的，但是我懒得改了。*

