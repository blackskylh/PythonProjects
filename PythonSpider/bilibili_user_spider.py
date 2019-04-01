# -*-coding:utf8-*-

import requests
import json
import random
import sys
import datetime
import time
from importlib import reload
import threading

def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()


reload(sys)

def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents("user_agents.txt")
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/45388',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

# 增加http代理列表，如果希望线程多，又不被B站防护机制block掉，就尽量增加多的代理
# B站对某个IP快速频繁的获取做了防护，因此目前对于1个代理，1s内只获取一次，None指不用代理（算作一个代理）
proxyips = [None,
            "1.2.3.4:1111"]

# 使用线程数量，一般比代理总数少1-2个
PROCESSES = 1

# 同一个代理连续10次读取失败，就会认为是个无效代理，被丢弃，当前读取失败的uid被重新加入uid池
THROWTIMES = 10

# 设置uid池，爬uid的范围
nums = list(range(3000000, 3000100))

class Proxy(object):
    def __init__(self, ip):
        self.proxy = None if ip is None else {"http" : "http://{}".format(ip)}
        self.count = 0

    def __str__(self):
        return str(self.proxy)


proxies = [Proxy(p) for p in proxyips]
lived_proxy = len(proxies)

time1 = time.time()

class BUser(object):
    def __init__(self, jsData):
        self.mid = jsData['mid']
        self.name = jsData['name']
        self.sex = jsData['sex']
        self.rank = jsData['rank']
        self.face = jsData['face']
        self.spacesta = jsData['spacesta']
        self.birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
        self.sign = jsData['sign']
        self.level = jsData['level_info']['current_level']
        self.officialVerifyType = jsData['official_verify']['type']
        self.officialVerifyDesc = jsData['official_verify']['desc']
        self.vipType = jsData['vip']['vipType']
        self.vipStatus = jsData['vip']['vipStatus']
        self.toutu = jsData['toutu']
        self.toutuId = jsData['toutuId']

    def format(self):
        return u"{u.mid},{u.name},{u.sex},{u.rank},{u.face},{u.spacesta},{u.birthday},{u.sign},{u.level},{u.officialVerifyType},\
{u.officialVerifyDesc},{u.vipType},{u.vipStatus},{u.toutu},{u.toutuId}\n\r".format(u=self)

    def write(self):
        s = self.format()
        with open("user_%d.csv" % (self.mid / 1000 * 1000), "a+") as f:
            f.write(s.encode("utf-8"))
        try:
            print(s)
        except Exception as e:
            pass

def ReadFromBilibili(uid, proxy):
    try:
        url = 'https://space.bilibili.com/' + str(uid)
        payload = {
            '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
            'mid': url.replace('https://space.bilibili.com/', '')
        }
        ua = random.choice(uas)
        head = {
            'User-Agent': ua,
            'Referer': 'https://space.bilibili.com/' + str(uid) + '?from=search&seid=' + str(random.randint(10000, 50000))
        }
        jscontent = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo',
                  headers=head,
                  data=payload,
                  proxies=proxy,
                  timeout=10).text
        time2 = time.time()

        jsDict = json.loads(jscontent)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                u = BUser(jsDict['data'])
                print ("proxy:{} fetch success!".format(proxy))
                u.write()
            else:
                print('no data now')
            return True
        else:
            print("Error: " + url)
            return True
    except Exception as e:
        print(e)
        print("uid:{}, proxy:{}".format(uid, proxy))

def ProcessRead(lock):
    global nums, proxies, lived_proxy
    while 1:
        lock.acquire()
        if len(nums) == 0:
            lock.release()
            print("thread exit!")
            return
        if lived_proxy == 0:
            print("Exist when no lived proxies.")
            lock.release()
            return
        if len(proxies) == 0:
            time.sleep(1)
            lock.release()
            print("No proxy, lived number is {}, waiting....".format(lived_proxy))
            continue
        num = nums.pop()
        proxy = proxies[0]
        proxies = proxies[1:]
        lock.release()

        time.sleep(1)
        success = ReadFromBilibili(num, proxy.proxy)
        
        lock.acquire()
        if not success:
            print("fetch failed, read num: {}".format(num))
            nums.append(num)

            proxy.count += 1
            if proxy.count >= THROWTIMES:
                print("delete proxy: {}".format(proxy))
                lived_proxy -= 1
            else:
                proxies.append(proxy)
        else:
            proxy.count = 0
            proxies.append(proxy)
        lock.release()

if __name__ == "__main__":
    lock = threading.RLock()
    pool = [threading.Thread(target=ProcessRead, args=(lock, )) for i in range(PROCESSES)]
    map(lambda p: p.start(), pool)
