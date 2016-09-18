# -*- coding: utf-8 -*- 

import urllib
import urllib2
import cookielib
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup

def login(user, passwrd):
	
	filename = 'cookie.txt'
	cookie = cookielib.MozillaCookieJar(filename)
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)

	url = "http://pt.vm.fudan.edu.cn/index.php?action=login2"

	data = {
		'user': user,
		'passwrd': passwrd,
		'cookielength': 1440
	}
	post_data = urllib.urlencode(data)
	r = opener.open(url, post_data)
	cookie.save(ignore_discard=True, ignore_expires=True)

def grade(name):
	names = name.split()
	name_after = "%20".join(names)
	grade_url = "https://movie.douban.com/subject_search?search_text=" + name_after + "&cat=1002"
	req = urllib2.Request(grade_url)
	response = urllib2.urlopen(req)

	html_doc = response.read()
	soup = BeautifulSoup(html_doc, "lxml")

	item = soup.find("span", {"class": "rating_nums"}).text
	return float(item)

def emailTo(mailbox, content):
	sender = ''

	message = MIMEText(content, 'plain', 'utf-8')
	message['From'] = Header(sender)
	message['To'] = Header(mailbox)

	subject = 'PT新资源'
	message['subject'] = Header(subject, 'utf-8')


	m_host = 'mail.fudan.edu.cn:25'
	m_user = sender
	m_password = ''
	server = smtplib.SMTP(m_host)
	server.ehlo()
	server.starttls()
	server.login(sender, m_password)
	server.sendmail(sender, [mailbox], message.as_string())
	print "email sent."
	server.close()


def PTCheck(urls):
	cookie = cookielib.MozillaCookieJar()
	
	cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

	prints = ""
	for url in urls:
		req = urllib2.Request(url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		response = opener.open(req)

		html_doc = response.read()
		soup = BeautifulSoup(html_doc, "lxml")

		rows = soup.find("table", {"class": "table_grid"}).find("tbody").findAll("tr")
		
		i = 0
		
		names = []
		
		for row in rows:
			if i > 24:
				break

			if i >= 1 : 
				cells = row.findAll("td")
				name = cells[2].span.getText()
				a = cells[4].find("strong")
				if a:
					try:
						g = grade(name.split('/')[0].strip())
						
					except Exception, e:
						print "excepting"
						prints += "Out of control:" + name
						prints += "\n"

					else:
						if g >= 7.0:
							print "succeed"
							prints += name
							prints += "  "
							prints += str(g)
							prints += "\n"
					
			i += 1
			time.sleep(0.1)
	return prints

user=""
passwrd=""


login(user, passwrd)
urls = ['https://pt.vm.fudan.edu.cn/index.php?board=25.0', 'https://pt.vm.fudan.edu.cn/index.php?board=24.0', 'https://pt.vm.fudan.edu.cn/index.php?board=23.0']
contents = PTCheck(urls)
emailTo(user, contents)