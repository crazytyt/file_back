
import sys
import requests
from bs4 import BeautifulSoup
import os

#导入所需要的模块
class idiom():

    html = ' '
    timeout = 60                    #默认超时时间为60秒
    headersParameters = {    #发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    def all_url(self, url):

        html = self.request(url)
        #print(html)
        self.parseContent(html)
        return

    def request(self, url):
        r = requests.get(url ,timeout=self.timeout, headers=self.headersParameters)
        if r.status_code==200:
            self.html = r.text
        else:
            self.html = u''
            print ('[ERROR]',self.url,u'get此url返回的http状态码不是200')
        #r.encoding = 'utf-8'
        r.encoding='gb2312'
        return r.text

    def parseContent(self, html):
        table = BeautifulSoup(html, 'lxml').find('table', id ='table1')
        for row in table.find_all("tr"):
            td = row.find_all("td")
            #cell = [i for i in td]
            print(" ==================")
            for row in td:
                img = row.find('img')
                print(img)
                print(" ---------------------------")

    '''
    def html(self, href):   ##获得图片的页面地址
        html = self.request(href)
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        #这个上面有提到
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url) ##调用img函数

    def img(self, page_url): ##处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url): ##保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path): ##创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("E:\mzitu2", path))
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(os.path.join("E:\mzitu2", path))
            os.chdir(os.path.join("E:\mzitu2", path)) ##切换到目录
            return True
        else:
            print( path, '文件夹已经存在了！')
            return False
    '''


#设置启动函数
if __name__ == '__main__':
    Idiom = idiom() ##实例化
    Idiom.all_url('http://www.hydcd.com/cy/fkccy/index.htm') ##给函数all_url传入参数  


'''
<table border="1" cellSpacing="0" borderColor="#BFBFFF" cellPadding="2" id="table1">
	<tr align="middle">
						<td width="170" height="210">
						<p>第53关</p>
						<p>
						<img border="0" src="images/CF92239-51.png" alt="八面来风"></p>
						<p><br><br>疯狂猜成语答案是:八面来风</td>
						<td width="170" height="210">
						<p>第54关</p>
						<p>
						<img border="0" src="images/CF92239-52.png" alt="话中有话"></p>
						<p><br><br>疯狂猜成语答案是:<a href="../htm2/hz4498.htm">话中有话</a></td>
						<td width="170" height="210">
						<p>第55关</p>
						<p>
						<img border="0" src="images/CF92239-50.png" alt="大跌眼镜"></p>
						<p><br><br>疯狂猜成语答案是:大跌眼镜</td>
						<td width="170" height="210">
						<p>第56关</p>
						<p>
						<img border="0" src="images/CF92239.png" alt="鸡犬升天"></p>
						<p><br><br>疯狂猜成语答案是:<a href="../htm2/jq5361.htm">鸡犬升天</a></td>
	</tr>
	<tr align="middle">
						<td width="170" height="210">
						<p>第57关</p>
						<p>
						<img border="0" src="images/CF92239-53.png" alt="日上三竿"></p>
						<p><br><br>疯狂猜成语答案是:<a href="../htm3/rs8545.htm">日上三竿</a></td>
						<td width="170" height="210">
						<p>第58关</p>
						<p>
						<img border="0" src="images/CF92240-50.png" alt="大显身手"></p>
						<p><br><br>疯狂猜成语答案是:<a href="../htm1/dx6286.htm">大显身手</a></td>
						<td width="170" height="210">
						<p>第59关</p>
						<p>
						<img border="0" src="images/CF92240.png" alt="逆水行舟"></p>
						<p><br><br>疯狂猜成语答案是:<a href="../htm3/ns4025.htm">逆水行舟</a></td>
						<td width="170" height="210">
						<p>第60关</p>
						<p>
						<img border="0" src="images/CF92240-51.png" alt="火烧眉毛"></p>
						<p><br><br>疯狂猜成语答案是:<a href="../htm2/hs5149.htm">火烧眉毛</a></td>
	</tr>'''
