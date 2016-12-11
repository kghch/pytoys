# za7za8

## lru_cache
shadowsocks-python版本中LRUCache的复制。

## PTCheck.py
筛选PT上三个热门板块最近两天内豆瓣评分>7.0的影片，发送到我邮箱。

## autoSign
[穿越时空](http://www.go-out.cc)自动签到脚本

## markdown_editor
markdown编辑器web端。

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