# -*- coding: utf-8 -*-
import requests
from lxml import etree

cook = {"Cookie": "_T_WM=5349e4ea3b0580d95cbde6822a123997; SUB=_2A257BI-TDeTxGeRP61cR8C7EyT6IHXVYBhHbrDV6PUJbrdANLUOtkW11SvF6cHF1qCLWKQlRdpPltNDtrA..; gsid_CTandWM=4u7V204b14UTNd37Zf5Mx8PBCdg"}
url = 'http://weibo.cn/u/2608591167'
html = requests.get(url, cookies = cook).content
# html = bytes(bytearray(html, encoding='utf-8'))
selector = etree.HTML(html)
content = selector.xpath('//span[@class="ctt"]')
for each in content:
	text = each.xpath('string(.)')
	print text
