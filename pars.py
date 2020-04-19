
from html.parser import HTMLParser
import re
import get_url
import requests

class MyHTMLParser(HTMLParser):
	strong = False
	name = ''
	processing = None
	stage = 0
	meaning = ""
	syn_ant = ''
	src = ''
	example = ''
	diangu = ''
	data = ''
	url = u''
	keyword = u''
	headersParameters = {    #发送HTTP请求时的HEAD信息，用于伪装为浏览器
		'Connection': 'Keep-Alive',
		'Accept': 'text/html, application/xhtml+xml, */*',
		'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
		'Accept-Encoding': 'gzip, deflate',
		'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	}


#	def handle_starttag(self, tag, attrs):

#	def handle_endtag(self, tag):

	def set_keyword(self, keyword):
		'''设置当前keyword'''
		print(" key word is " + keyword)
		self.url = u'nyu.baidu.com/s?wd='+keyword+'&ptype=zici&tn=sug_click#detailmean'
	def set_url(self, url):
		'''设置当前url'''
		self.url = url
	def get_html(self):
		r = requests.get(self.url , 60, headers=self.headersParameters)
		r.encoding = None
		if r.status_code==200:
			print(r.text)
			return r.text
		else:
			self.html = u''
			print ('[ERROR]',self.url,u'get此url返回的http状态码不是200')


	def handle_data(self, data):
		self.data += data
	
	def handle_comment(self, data):
		print("comments:" + data + "?")
		if data == ' 头部 ':
			self.stage = 1
			self.data = '' 
		if data == ' 解释 ':
			self.name = self.data
			self.stage = 2
			self.data = '' 
		if data == ' 出处 ':
			self.meaning = self.data
			self.stage = 3
			self.data = '' 
		if data == ' 例句 ':
			self.src = self.data
			self.stage = 4
			self.data = '' 
		if data == ' 近反义词 ':
			self.example = self.data
			self.stage = 5
			self.data = '' 
		if data == " 典故 ":
			self.syn_ant = self.data
			self.stage = 6
			self.data = '' 
		if data == " 成语接龙 ":
			self.diangu = self.data
			self.stage = 7
			mm = re.search(r'(【解释】.*?)', self.meaning, re.M|re.I)
			ss = re.search(r'(【出自】.*)', self.meaning, re.M|re.I)
			ee = re.search(r'(【示例】.*)', self.meaning, re.M|re.I)
			yy = re.search(r'(【语法】.*)', self.meaning, re.M|re.I)
			print(self.meaning)
			print(mm.group(0))

#print(mm + ':' + ss + ':' + ee + ':' + yy)
			#print('name: '+self.name + 'meaning: '+ self.meaning+
			#		'src: '+self.src+'example: '+self.example+
			#		'syn_ant: '+self.syn_ant+'diangu: '+self.diangu)

#fi = open('./fengjing.txt', 'r')
#text = fi.read()
#text = '自相矛盾'
text = input("Input the idiom: ")

parser = MyHTMLParser()
parser.set_keyword(text)
tt = parser.get_html()
parser.feed(tt)
