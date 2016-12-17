# -*- coding: utf-8 -*-

import os
import shutil
import time
import ConfigParser
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

session = requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Referer': 'http://www.zhihu.com/'
}

for key, value in enumerate(headers):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

driver = webdriver.PhantomJS(executable_path=r'E:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')

cf = ConfigParser.ConfigParser()
cf.read('zhihu_config.ini')
cookies_config = dict(cf.items('cookies'))

def login():
    """ 用cookies登录，所以这一步只是加了cookies """
    for name, value in cookies_config.items():
        driver.add_cookie({"name": name, "value": value, "domain": ".zhihu.com", "path": "/"})

def scroll_to_bottom(start):
    js = "window.scrollTo(0, document.body.scrollHeight);"
    driver.execute_script(js)
    time.sleep(0.8)


def user_posts(username, opt):
    """ 输入username, opt[posts, answers]，返回该user的所有回答/文章 """
    if opt == 'posts':
        url = 'https://www.zhihu.com/people/' + username + '/posts'
    elif opt == 'answers':
        url = 'https://www.zhihu.com/people/' + username + '/answers'
    else:
        return
    print 'Starting spying from the root: ' + url
    driver.get(url)
    old = len(driver.page_source)
    while True:
        scroll_to_bottom(old)
        new = len(driver.page_source)
        if new <= old:
            break
        else:
            old = new

    return_js = "return document.getElementsByClassName('ContentItem-content is-collapsed')"
    driver.execute_script(return_js)
    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, "html.parser")
    content_items = soup.findAll("div", {"class": "ContentItem"})

    posts = []
    for item in content_items:
        e_item = item.find("h2", {"class": "ContentItem-title"})
        posts.append(e_item)
    return len(content_items), posts


def each_answer(url):
    """ 根据回答的url，返回该答案内容 """
    r = session.get(url, headers=headers, cookies=cookies_config)
    html_doc = r.content
    soup = BeautifulSoup(html_doc, "html.parser")
    try:
        ans = soup.find("div", {"class": "zm-item-rich-text expandable js-collapse-body"}).find("div", {"class": "zm-editable-content clearfix"})
    except AttributeError:
        print "[Warning] Can't parse answer from " + url
        return "empty"
    else:
        ans = str(ans)
        ans = re.sub(r'src="//[^"]+"', '', ans)
        ans = re.sub(r'data-actualsrc', 'src', ans)
        ans = ans.replace('href="//link.zhihu.com/?target=', 'href="')
        ans = ans.replace('https%3A', 'https:')
        ans = ans.replace('http%3A', 'http:')
        return ans


def do_spider(user):
    login()
    subdir_name = user + '/' + user + '_answers'
    if os.path.exists(user):
        print "Deleting old %s folder" % user
        shutil.rmtree(user)

    os.makedirs(user)
    if not os.path.exists(subdir_name):
        os.makedirs(subdir_name)

    if not os.path.exists('cache/' + user):
        if not os.path.exists('cache'):
            os.makedirs('cache')
        num, posts = user_posts(user, 'answers')
        print ("答案数： %s") % num
        urls = []
        questions = []
        with open('cache/' + user, 'a+') as f:
            for post in posts:
                url = 'https://www.zhihu.com' + post.find('a').get('href')
                question = post.find('a').getText()
                urls.append(url)
                questions.append(question)
                f.write(question.encode("utf-8"))
                f.write('\n')
                f.write(url.encode("utf-8"))
                f.write('\n')
    else:
        # read answers from cache
        with open('cache/' + user, 'r') as f:
            lines = f.readlines()
            questions = lines[0::2]
            urls = lines[1::2]
            num = len(urls)
        print "Using cache..."
        print ("答案数： %s") % num

    style = """<!DOCTYPE html><head><style>body{padding: 50px;}</style></head>"""
    title = ('用户%s的答案数%s：') % (user, num)

    index_file = user + '/' + 'index.html'
    with open(index_file, 'a+') as f:
        f.write(style.encode("utf-8"))
        f.write(title)

    answers_url = []
    success_num = 0

    for i in range(num):
        time.sleep(0.4)
        url = urls[i]
        print url
        question = questions[i]
        answers_url.append(url)
        file_name = url[url.find('answer/')+7:]
        file_pos = subdir_name + '/' + file_name + '.html'
        ans_html = each_answer(url)
        if ans_html != "empty":
            success_num += 1
            question_link = '<h3><a href="' + user + '_answers/' + file_name + '.html' +'">Question:  ' + question + '</a></h3><br/>'
            question_title = '<h3>' + question + '</h3><br/>'
            with open(index_file, 'a+') as f:
                f.write(question_link.encode("utf-8"))

            style = """<!DOCTYPE html><head><link rel="stylesheet" type="text/css" href="../../z.css" /></head>"""
            with open(file_pos, 'a+') as f:
                f.write(question_title.encode("utf-8"))
                f.write(style.encode("utf-8"))
                f.write(ans_html)
    print ("抓取数： %s") % success_num

    ending = ('抓取数: %s') % success_num
    with open(index_file, 'a+') as f:
        f.write(ending)

if __name__ == "__main__":
    do_spider('qcboy')
