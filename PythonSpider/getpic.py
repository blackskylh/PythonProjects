
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import re
import os

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def make_header(user_agent):
    return {'User-Agent': user_agent}

def getURL(url,regex):

    # 正则表达式，得到图片地址
    try:
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        # content = response.read()
        content = BeautifulSoup(response, 'lxml')
    except urllib.error.HTTPError as e:
        print(e)
        exit()
    except urllib.error.URLError as e:
        print(e)
        exit()
    print(content)
    '''
    filepath = path + 'content.txt'
    f = open(filepath, 'w', encoding='utf-8')
    f.write(content.decode('utf-8', 'ignore'))
    f.close()
    '''
    # 提取数据
    # return re.findall(regex, content.decode('utf-8', 'ignore'))
    return content.find("ul", class_="nav-menu").findAll("a")

def save(items):
    count = 0
    # 保存信息
    for item in items:
        count += 1
        print('第' + str(count) + '张')
        '''
        if item.find('ttps') == 0:
            item = 'h'+item
        else:
            item = 'https:/'+item'''
        print(item.attrs['href'])

        # 打开items中保存的图片网址，并下载图片保存在本地，format格式化字符串
        #urllib.request.urlretrieve(item, '{}/{}.{}'.format(path, count, item[-3:]))
    print('完成')

if __name__ == '__main__':
    # 访问网址并抓取源码
    path = './pic'
    make_dir(path)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    headers = make_header(user_agent)
    # 正则表达式，得到图片地址
    reg = r'<img src="[^\"](.*?\.(?:jpg|png|gif))" (?:width|alt)'
    # reg = r'<a href="//.*?">[^\s](?:\!|span)'
    regex = re.compile(reg)
    url = 'http://www.bilibili.com'
    items = getURL(url, regex)
    print(items)
    save(items)

