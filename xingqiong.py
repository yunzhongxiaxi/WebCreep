import re
import time

import pymysql
import requests
import json

from heping import sendemail

class Order:
    def __init__(self, email: int, time: int, musthave: [],maxprice:int):
        self.email = email
        self.endtime = time+ time.time()
        self.musthave = musthave
        self.maxprice=maxprice
def judgecondition(maxprice,musthave,des,price):
    if maxprice<price or price is None:
        return 0
    for tmp in musthave:
        if tmp not in  des:
            return 0
    return 1
def getdata(mydb):
    url = "https://api.pzds.com/api/web-client/v2/public/goodsPublic/page"
    payload = '{"action":{"keywords":[],"merchantMark":null,"goodsCatalogueId":6,"gameId":213},"sort":"createTime","order":"DESC","page":1,"pageSize":100}'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '138',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'api.pzds.com',
        'Origin': 'https://www.pzds.com',
        'PZOs': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'PZPlatform': 'pc',
        'PZTimestamp': '111',
        'PZVersion': '3.7.0',
        'PZVersionCode': '1',
        'Referer': 'https://www.pzds.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'channelInfo': '{"channelCode":null,"tag":null,"channelType":null,"searchWord":"null"}',
        'instance': 'false',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'signSkip': 'true'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        print(0)
        mydict = json.loads(response.text)
        a = mydict['data']['records']
        for tmp in a:
            bianhao = tmp['goodsNo']
            mysearch = "select * from xingqiong where bianhao='{bianhao}'".format(bianhao=bianhao)
            cursor.execute(mysearch)
            if not len(cursor.fetchall()):
                title = tmp['title']
                des=title
                price=tmp['price']
#判断条件
                if judgecondition(maxprice=1000, musthave=['卡芙卡','镜流','罗刹'], des=des,price=price)==1:
                    sendemail(title,price,'2723513948@qq.com') #3.27
                sql = "insert into xingqiong(bianhao,title,price) values('{bianhao}','{title}','{price}')".format(
                    bianhao=bianhao,title=title[:1000],price=price)
                cursor.execute(sql)
                mydb.commit()
    except  Exception as e:
        mydb.rollback()
        print('getdata:' + e.__str__())

def getpangxiedata(mydb):
    url = "https://api.pxb7.com/api/product/list?game_id=161&rec=&category=%7B%221%22:0,%222%22:[],%223%22:[],%226%22:[],%227%22:[],%228%22:[],%229%22:[],%2210%22:[],%2211%22:[],%2212%22:[],%2213%22:[],%2214%22:[],%2215%22:[],%2216%22:[],%2217%22:0,%2218%22:0,%2220%22:0,%2221%22:0,%2222%22:0,%2223%22:0,%2224%22:0%7D&scope=%7B%22min_price%22:%22%22,%22max_price%22:%22%22,%22min_v_number%22:%22%22,%22max_v_number%22:%22%22,%22min_server%22:%22%22,%22max_server%22:%22%22%7D&services=all&sort=%7B%22type%22:%22isnew%22,%22method%22:1%7D&page=1"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Apitoken': '8be5ef37f13814797d41b01b62c60a64',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Dnt': '1',
        'Host': 'api.pxb7.com',
        'Loginstatus': 'false',
        'Token': 'a87ff679a2f3e71d9181a67b7542122c',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0:',
        'Cookie': 'acw_tc=1b5d0de72e2c602a3735bd7238338041876058f9989e04ea2f9f02c80b5d1847; aliyungf_tc=abecc25dccacb84f413834dda1f60ae2b5632cf132781a2b3aca7c43c7bcf6a5'
    }
    try:

        response = requests.request("GET", url, headers=headers, data=payload)
        print(1)
        mydict = json.loads(response.text)
        a = mydict['data']['list']
        for tmp in a:
            title=str(tmp['name'])
            prebianhao=re.search('【(\w+)】',title)
            if prebianhao is None:
                continue
            bianhao=prebianhao.group(1)
            mysearch = "select * from xingqiong where bianhao='{bianhao}'".format(bianhao=bianhao)
            cursor.execute(mysearch)
            if  not len(cursor.fetchall()):
                price=int(tmp['price'])
                des=title
                if judgecondition(maxprice=1000, musthave=['卡芙卡','镜流','罗刹'], des=des,price=price)==1:
                    sendemail(title,price,'2723513948@qq.com') #3.27
                    #print(1)
                sql = "insert into xingqiong(bianhao,title,price) values('{bianhao}','{title}',{price})".format(
                    bianhao=bianhao,title=title[:1000],price=price)
                cursor.execute(sql)
                mydb.commit()
    except  Exception as e:
        mydb.rollback()
        print('getpangxiedata:' + e.__str__())

if __name__ == '__main__':
    db=None
    try:
        db = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='panzhi')
        print('连接成功！')
    except Exception as e:
        print('something wrong!')
    cursor = db.cursor()
    while True:
        getdata(db)
        getpangxiedata(db)
        time.sleep(60)