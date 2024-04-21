import json
import re
import time

import pymysql
import requests

from heping import sendemail
def judge(huang,price):
    if huang >= 50 and price <= 300:
        return 1
    if huang >= 60 and price <= 400:
        return 1
    if huang >= 70 and price <= 500:
        return 1
    return 0
def judge1(des,price,email):
    # if '【未绑定邮箱】' not in des and '【送网易未实名邮箱】' not in des:
    #     return 1
    if '6命芙宁娜' not in des:
        return 1
    count=0
    if '6命雷电将军' in des:
        count+=1
    if '6命八重神子' in des:
        count+=1
    if '6命霄宫' in des:
        count+=1
    if '6命纳西妲' in des:
        count+=1
    if '6命夜兰' in des:
        count += 1
    if count<3:
        return 1
    if price >6000:
        return 1
    sendemail(des,price,email)
    return 0
def judge2(des,price,email):
    # if '【未绑定邮箱】' not in des and '【送网易未实名邮箱】' not in des:
    #     return 1
    liuming=re.search('六命：([\s\S]*)五命',des)
    if liuming is  None:
        return 1
    des=liuming.group(1)
    if '芙宁娜' not in des:
        return 1
    count=0
    if '雷电将军' in des:
        count+=1
    if '八重神子' in des:
        count+=1
    if '霄宫' in des:
        count+=1
    if '纳西妲' in des:
        count+=1
    if '夜兰' in des:
        count += 1
    if '神里凌华' in des:
        count+=1
    if count<3:
        return 1
    if price >6000:
        return 1
    sendemail(des,price,email)
    return 0
def getyuanshendata(mydb):
    url = "https://api.pzds.com/api/web-client/v2/public/goodsPublic/page"
    payload = '{"action":{"keywords":[],"merchantMark":null,"goodsCatalogueId":6,"gameId":12},"sort":"createTime","order":"DESC","page":1,"pageSize":100}'
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
    response = requests.request("POST", url, headers=headers, data=payload)
    mydict = json.loads(response.text)
    a = mydict['data']['records']
    try:
        for tmp in a:
            bianhao = tmp['goodsNo']
            mysearch = "select * from yuanshen where bianhao='{bianhao}'".format(bianhao=bianhao)
            cursor.execute(mysearch)
            if not len(cursor.fetchall()):
                des = tmp['title']
                price=tmp['price']
                pre= re.search('，([0-9]+)黄，', des)
                huang=0 if pre is  None else int(pre.group(1))
                if judge(huang,price)==1:
                    sendemail(des,price,'15211006993@163.com')
                judge1(des,price,'2339917384@qq.com')
                sql = "insert into yuanshen(bianhao,price,des,huang) values('{bianhao}',{price},'{title}',{huang})".format(
                    bianhao=bianhao, title=des[:1000], huang=huang, price=price)
                cursor.execute(sql)
                mydb.commit()
    except  Exception as e:
        mydb.rollback()
        print('getdata:' + e.__str__())
def getpangxiedata(mydb):
    url = "https://api.pxb7.com/api/product/list?game_id=26&rec=&category=%7B%221%22:0,%222%22:[],%223%22:[],%225%22:0,%226%22:0,%228%22:0,%2210%22:[],%2215%22:[],%2216%22:[],%2217%22:[],%2218%22:[],%2219%22:[],%2222%22:[],%2223%22:[],%2224%22:[],%2225%22:[],%2226%22:[],%2227%22:0,%2228%22:0%7D&scope=%7B%22min_price%22:%22%22,%22max_price%22:%22%22,%22min_yellow%22:%22%22,%22max_yellow%22:%22%22,%22min_role_count%22:%22%22,%22max_role_count%22:%22%22,%22min_adventure_level%22:%22%22,%22max_adventure_level%22:%22%22%7D&services=all&sort=%7B%22type%22:%22isnew%22,%22method%22:1%7D&page=1"
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

    response = requests.request("GET", url, headers=headers, data=payload)
    # data = brotli.decompress(response.content)
    # data1 = data.decode('utf-8')
    # print(data1)
    mydict = json.loads(response.text)
    a = mydict['data']['list']
    try:
        for tmp in a:
            title=tmp['name']
            prebianhao=re.search('【(\w+)】',title)
            if prebianhao is None:
                continue
            bianhao=prebianhao.group(1)
            mysearch = "select * from yuanshen where bianhao='{bianhao}'".format(bianhao=bianhao)
            cursor.execute(mysearch)
            if  not len(cursor.fetchall()):
                price=int(tmp['price'])
                pre = re.search('，([0-9]+)黄，', title)
                huang = 0 if pre is None else int(pre.group(1))
                if judge(huang,price)==1:
                    sendemail(title,price,'15211006993@163.com')
                judge2(title,price,'2339917384@qq.com')
                sql = "insert into yuanshen(bianhao,price,des,huang) values('{bianhao}',{price},'{title}',{huang})".format(
                    bianhao=bianhao, title=title[:1000], huang=huang, price=price)
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
        getyuanshendata(db)
        getpangxiedata(db)
        time.sleep(60)
