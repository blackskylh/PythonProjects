
import urllib.request
import urllib.error
import re
import os

if __name__ == '__main__':
    # 访问网址并抓取源码
    path = './qiubai'
    if not os.path.exists(path):
        os.makedirs(path)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    headers = {'User-Agent': user_agent}
    regex = re.compile('<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S)
    count = 1
    for cnt in range(1, 35):
        print('第' + str(cnt) + '轮')
        url = 'http://www.qiushibaike.com/textnew/page/' + str(cnt) + '/?s=4941357'
        try:
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request)
            content = response.read()
        except urllib.error.HTTPError as e:
            print(e)
            exit()
        except urllib.error.URLError as e:
            print(e)
            exit()
        print(content)

        # 提取数据
        # 注意换行符，设置 . 能够匹配换行符
        items = re.findall(regex, content.decode('utf-8', 'ignore'))

        # 保存信息
        for item in items:
            #   print item
            #   整理数据，去掉\n,将<br/>换成\n
            item = item.replace('\n', '').replace('<br/>', '\n')
            filepath = path + '/' + str(count) + '.txt'
            f = open(filepath, 'w', encoding='utf-8')
            f.write(item)
            f.close()
            count += 1
        print('完成')
