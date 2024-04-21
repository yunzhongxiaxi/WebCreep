import json
import re
import time
import pymysql
import requests
import smtplib
import execjs

from email.mime.text import MIMEText
def sendemail(content, price,email):
    mail_user = 'vjmbsd'
    mail_pass = 'HVYZEVNOSEOYSADS'
    sender = 'vjmbsd@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [ email]

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = f'总价：{price}'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = ';'.join(receivers)
    # 登录并发送邮件
    try:
        # 连接到服务器

        smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
        # 登录到服务
        smtp.login(mail_user, mail_pass)
        # 发送
        smtp.sendmail(sender, receivers, message.as_string())
        # 退出
        smtp.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误

# def sendemail(content, price,email):
#     mail_host = 'smtp.163.com'
#     mail_user = 'vjmbsd'
#     mail_pass = 'HVYZEVNOSEOYSADS'
#     sender = 'vjmbsd@163.com'
#     # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
#     receivers = [ email]
#
#     # 设置email信息
#     # 邮件内容设置
#     message = MIMEText(content, 'plain', 'utf-8')
#     # 邮件主题
#     message['Subject'] = f'总价：{price}'
#     # 发送方信息
#     message['From'] = sender
#     # 接受方信息
#     message['To'] = ';'.join(receivers)
#
#     # 登录并发送邮件
#     try:
#         smtp_obj = smtplib.SMTP()
#         # 连接到服务器
#         smtp_obj.connect(mail_host, 25)
#         # 登录到服务器
#         smtp_obj.login(mail_user, mail_pass)
#         # 发送
#         smtp_obj.sendmail(sender, receivers, message.as_string())
#         # 退出
#         smtp_obj.quit()
#         print('success')
#     except smtplib.SMTPException as e:
#         print('error', e)  # 打印错误
def js_from_file(file_name):
    """
    读取js文件
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result
def getdata(mydb):
    url = "https://api.pzds.com/api/web-client/v2/public/goodsPublic/page"
    payload = '{"action":{"keywords":[],"merchantMark":null,"goodsCatalogueId":6,"gameId":8},"sort":"createTime","order":"DESC","page":1,"pageSize":100}'
    context1 = execjs.compile(js_from_file('./test.js'))
    result1 = context1.call("myJiaMi",str(payload))
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '136',
    'Content-Type': 'application/json;charset=UTF-8',
    'DNT': '1',
    'Host': 'api.pzds.com',
    'PZOs': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'PZPlatform': 'pc',
    'PZTimestamp': str(result1['Timestamp']),
    'PZVersion': '1.0.0',
    'PZVersionCode': '1',
    'Random': str(result1['Random']),
    'Sign': str(result1['strMd5']),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'channelInfo': '{"channelCode":null,"tag":null,"channelType":null,"searchWord":"null"}',
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        print(0)
        mydict = json.loads(response.text)
        a = mydict['data']['records']
        for tmp in a:
            bianhao = tmp['goodsNo']
            mysearch = "select * from heping where bianhao='{bianhao}'".format(bianhao=bianhao)
            cursor.execute(mysearch)
            if not len(cursor.fetchall()):
                des = tmp['title']
                price=tmp['price']
                keerci= re.search('不可二次实名', des) is None
                dushi=re.search('套装-都市猎人',des) is not  None
                chixie=re.search('套装-赤蝎幽灵',des) is not  None
                paidui=re.search('套装-派对舞王', des) is not None
                res=re.search('([0-9]+)载具',des)
                zaiju=0 if res is None else int(res.group(1))
                if keerci and dushi and paidui and chixie and price<=5000 and zaiju>=3:
                    sendemail(des,price,'1223309133@qq.com')
                sql = "insert into heping(bianhao,title) values('{bianhao}','{title}')".format(
                    bianhao=bianhao,title=des[:1000])
                cursor.execute(sql)
                mydb.commit()
    except  Exception as e:
        mydb.rollback()
        print('getdata:' + e.__str__())
def getpangxiedata(mydb):
    url = "https://api.pxb7.com/api/product/list?game_id= 11&rec= &category= %7B%221%22:0,%222%22:[],%223%22:[],%224%22:[],%225%22:[],%227%22:0,%228%22:0,%229%22:[],%2210%22:[],%2211%22:[],%2212%22:[]%7D&scope= %7B%22min_price%22:%22%22,%22max_price%22:%22%22,%22min_credit%22:%22%22,%22max_credit%22:%22%22,%22min_cars%22:%22%22,%22max_cars%22:%22%22%7D&services= all&sort= %7B%22type%22:%22isnew%22,%22method%22:1%7D&page= 1"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Apitoken': 'bc45910aeffb9ab747057b9fdaf46a19',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Dnt': '1',
        'Host': 'api.pxb7.com',
        'Loginstatus': 'false',
        'Token': '41b114b8e98778594c30b61b2b05322e',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0:',
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(1)
        mydict = json.loads(response.text)
        a = mydict['data']['list']
        for tmp in a:
            title=tmp['name']
            prebianhao=re.search('【(\w+)】',title)
            if prebianhao is None:
                continue
            bianhao=prebianhao.group(1)
            mysearch = "select * from heping where bianhao='{bianhao}'".format(bianhao=bianhao)
            cursor.execute(mysearch)
            if  not len(cursor.fetchall()):
                price=int(tmp['price'])
                keerci= re.search('不可二次实名', title) is None
                dushi=re.search('都市猎人',title) is not  None
                chixie=re.search('赤蝎幽灵',title) is not  None
                paidui=re.search('派对舞王', title) is not None
                res=re.search('([0-9]+)载具',title)
                zaiju=0 if res is None else int(res.group(1))
                if keerci and dushi and paidui and chixie and price<=5000:
                    sendemail(title,price,'1223309133@qq.com')
                sql = "insert into heping(bianhao,title) values('{bianhao}','{title}')".format(
                    bianhao=bianhao,title=str(title)[:1000])
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
        print(e.__str__())
    cursor = db.cursor()
    while True:

        getdata(db)
        getpangxiedata(db)
        time.sleep(60)
