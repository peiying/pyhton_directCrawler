# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import requests
from lxml import etree
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class mailhelper(object):
    '''
    实现发送邮件的功能
    '''
    def __init__(self):

        self.mail_host="smtp.163.com"  #设置服务器
        self.mail_user="ypypatricka"    #用户名
        self.mail_pass="patricka0612"   #密码
        self.mail_postfix="163.com"  #发件箱的后缀

    def send_mail(self,to_list,sub,content):
        me="xxoohelper"+"<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False

class xxoohelper(object):
    '''
    这个类实现将爬取微博第一条内容
    '''
    def __init__(self):
        #self.url = 'http://weibo.cn/u/2608591167' #请输入准备抓取的微博地址
        self.url = 'http://weibo.cn/nvliu66?vt=4'
        self.url_login = 'https://login.weibo.cn/login/'
        self.new_url = self.url_login

    def getSource(self):
        html = requests.get(self.url).content
        return html

    # def getData(self,html):
    #     selector = etree.HTML(html)
    #     password = selector.xpath('//input[@type="password"]/@name')[0]
    #     vk = selector.xpath('//input[@name="vk"]/@value')[0]
    #     action = selector.xpath('//form[@method="post"]/@action')[0]
    #     self.new_url = self.url_login + action
    #     data = {
    #         'mobile' : 'xxxxx@xxx.com',
    #          password : 'xxxxxx',
    #         'remember' : 'on',
    #         'backURL' : 'http://weibo.cn/u/xxxxxx', #此处请修改为微博地址
    #         'backTitle' : u'微博',
    #         'tryCount' : '',
    #         'vk' : vk,
    #         'submit' : u'登录'
    #         }
    #     return data

    # def getContent(self,data):
    #     newhtml = requests.post(self.new_url,data=data).content
    #     new_selector = etree.HTML(newhtml)
    #     content = new_selector.xpath('//span[@class="ctt"]')
    #     newcontent = unicode(content[2].xpath('string(.)')).replace('http://','')
    #     sendtime = new_selector.xpath('//span[@class="ct"]/text()')[0]
    #     sendtext = newcontent + sendtime
    #     return sendtext

    def getContent(self):
        cook = {"Cookie": "_T_WM=5349e4ea3b0580d95cbde6822a123997; SUB=_2A257BI-TDeTxGeRP61cR8C7EyT6IHXVYBhHbrDV6PUJbrdANLUOtkW11SvF6cHF1qCLWKQlRdpPltNDtrA..; gsid_CTandWM=4u7V204b14UTNd37Zf5Mx8PBCdg"}
        sendContent = {}
        #url = 'http://weibo.cn/u/2608591167'
        html = requests.get(self.url, cookies = cook).content
        selector = etree.HTML(html)
        content = selector.xpath('//span[@class="ctt"]')
        sendContent[0] = unicode(content[4].xpath('string(.)')).replace('http://','')
        sendContent[1] = selector.xpath('//span[@class="ct"]/text()')[1]
        # newcontent = unicode(content[4].xpath('string(.)')).replace('http://','')
        # sendtime = selector.xpath('//span[@class="ct"]/text()')[1]
        #sendtext = newcontent + sendtime
        return sendContent

    def tosave(self,text):
        f= open('weibo.txt','a')
        f.write(text + '\n')
        f.close()

    def tocheck(self,data):
        if not os.path.exists('weibo.txt'):
            return True
        else:
            f = open('weibo.txt', 'r')
            existweibo = f.readlines()
            if data in existweibo:
                return False
            else:
                return True 


if __name__ == '__main__':
    mailto_list=['277079165@qq.com'] #此处填写接收邮件的邮箱
    helper = xxoohelper()
    i = 0;
    while i < 2:
        content = helper.getContent()
        sentContent = content[0]
        sentTime = content[1]
        allContent = sentContent + sentTime
        if helper.tocheck(sentContent):
            if mailhelper().send_mail(mailto_list,u"女神更新啦",allContent):
                print u"发送成功"
            else:
                print u"发送失败"
            helper.tosave(allContent)
        else:
            print u'无更新'
        time.sleep(10)
        i += 1
        print i