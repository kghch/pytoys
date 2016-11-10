# -*- coding: utf-8 -*- 

import urllib
import urllib2
import cookielib
import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header


def login(user, passwrd):
    
    filename = 'cookie_signin.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)

    url = "http://www.go-out.cc/user/_login.php"

    data = {
        'email': user,
        'passwd': passwrd,
		'remember_me': 'week'
    }
    post_data = urllib.urlencode(data)
    r = opener.open(url, post_data)

    cookie.save(ignore_discard=True, ignore_expires=True)

def emailTo(sender, receiver, title, content, password):
	
	dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

	content = content + '\n' + dt
	message = MIMEText(content, 'plain', 'utf-8')
	message['From'] = Header(sender)
	message['To'] = Header(receiver)
	message['subject'] = Header(title, 'utf-8')
	
	m_host = 'mail.fudan.edu.cn:25'
	server = smtplib.SMTP(m_host)
	server.ehlo()
	server.starttls()
	server.login(sender, password)
	server.sendmail(sender, [receiver], message.as_string())
	server.close()
	
	
def autoSign(sign_url):
	cookie = cookielib.MozillaCookieJar()
	cookie.load('cookie_signin.txt', ignore_discard=True, ignore_expires=True)
	req = urllib2.Request(sign_url)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open(req)
	return response.code
    
	
user = 'wanghan0307@gmail.com'
passwrd = 'password for go-out.cc'

login(user, passwrd)
sign_url = 'http://www.go-out.cc/user/_checkin.php'

res = autoSign(sign_url)


if res == 200:
	sender = '15210240044@fudan.edu.cn'
	receiver = '15210240044@fudan.edu.cn'
	password = 'password for email'
	emailTo(sender, receiver, 'AugoSign', 'Success', password)
else:
	emailTo(sender, receiver, 'Error for AutoSign', ' ', password)