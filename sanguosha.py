import json
import re
import time
import traceback
import execjs
import pymysql
import requests
import smtplib
from email.mime.text import MIMEText

from heping import js_from_file

class AccountChecker:
    def __init__(self):
        self.db = self.connect_database()
        self.cursor = self.db.cursor()
        self.bianhao=''
        self.wujiang=''
        self.price=0
        self.des = ''
    def judgecondition(self, item):
        if '倚星折月' in self.des and '匡汉延祚' in self.des and '神郭嘉' in self.wujiang and '神荀彧' in self.wujiang and self.price<=9000:
            return 1
        if item[2]<self.price:
            return 0
        s=str(item[1])
        wujiangs= s.split(',')
        for wujiang in wujiangs:
            if wujiang not in self.wujiang:
                return 0
        return 1

    @staticmethod
    def connect_database():
        try:
            return pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, db='panzhi')
        except Exception as e:
            print(f'Database connection failed: {e}')
            exit()

    @staticmethod
    def send_email(content, email, myprice):
        mail_host = 'smtp.163.com'
        mail_user = 'vjmbsd'
        mail_pass = 'HVYZEVNOSEOYSADS'
        sender = 'vjmbsd@163.com'
        receivers = [email] if email else ['2391860056@qq.com']

        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = f'Total Price: {myprice}'
        message['From'] = sender
        message['To'] = ';'.join(receivers)

        try:
            smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
            # 登录到服务
            smtp.login(mail_user, mail_pass)
            # 发送
            smtp.sendmail(sender, receivers, message.as_string())
            # 退出
            smtp.quit()
            print('Email sent successfully')
        except smtplib.SMTPException as e:
            print(f'Error sending email: {e}')

    @staticmethod
    def parse_description(origin):
        pre = re.search('【订单编号】([\s\S]*?)【其他皮肤】', origin)
        return pre.group(1) if pre else ''

    def check_and_notify_users(self):
        try:
            with self.db.cursor() as cursor:
                sql = "SELECT * FROM sanguosha_user WHERE expiration_date >= CURDATE()"
                cursor.execute(sql)
                users = cursor.fetchall()

                for user in users:
                    sql = f"SELECT * FROM sanguosha_user_item WHERE user_id = {user[0]}"
                    cursor.execute(sql)
                    items = cursor.fetchall()
                    for item in items:
                        if self.judgecondition(item)==1:
                            self.send_email(
                                f"Found a matching account: {self.des}",
                                user[1],
                                self.price
                            )
                            break

        except Exception as e:
            print(f"Error checking and notifying users: {e}")

    def getpanzhidata(self):
        url = "https://api.pzds.com/api/web-client/v2/public/goodsPublic/page"
        payload = '{"action":{"keywords":[],"merchantMark":null,"goodsCatalogueId":6,"single1":2209,"single2":null,"single3":null,"gameId":43},"sort":"createTime","order":"DESC","page":1,"pageSize":100}'
        context1 = execjs.compile(js_from_file('test.js'))
        result1 = context1.call("myJiaMi", str(payload))
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '136',
            'Channelinfo':'{"channelCode":null,"tag":null,"channelType":null,"searchWord":"null"}',
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
            response = requests.request('post', url, headers=headers, data=payload)
            mydict = json.loads(response.text)
            a = mydict['data']['records']
            for tmp in a:
                self.bianhao = tmp['goodsNo']
                self. price = tmp['price']
                self.des=tmp['title']
                self.wujiang = self.des
                mysearch = "select * from sanguosha where bianhao='{bianhao}'".format(bianhao=self.bianhao)
                self.cursor.execute(mysearch)
                if not len(self.cursor.fetchall()):
                    self.check_and_notify_users()
                    sql = "insert into sanguosha(bianhao,price,des) values('{bianhao}',{price},'{des}') ".format(
                        bianhao=self.bianhao, price=self.price, des=self.des[:500])
                    self.cursor.execute(sql)
                    self.db.commit()
        except  Exception as e:
            print('getpanzhidata:' + e.__str__())

    def getpangxiedata(self):
        url = "https://api.pxb7.com/api/product/list?game_id=61&rec=&category=%7B%221%22:0,%222%22:0,%223%22:0,%224%22:0,%229%22:[],%2211%22:[],%2212%22:[],%2213%22:[],%2214%22:[],%2215%22:[],%2216%22:[]%7D&scope=%7B%22min_price%22:%22%22,%22max_price%22:%22%22%7D&services=all&sort=%7B%22type%22:%22isnew%22,%22method%22:1%7D&page=1"
        payload = {
            "game_id": 61,
            "rec": "",
            "category": {
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0,
                "9": [],
                "11": [],
                "12": [],
                "13": [],
                "14": [],
                "15": [],
                "16": []
            },
            "scope": {
                "min_price": "",
                "max_price": ""
            },
            "services": "all",
            "sort": {
                "type": "isnew",
                "method": 1
            },
            "page": 1
        }
        context2 = execjs.compile(js_from_file('pangxiejiami.js'))
        result2 = context2.call("pangxie", payload)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'ApiToken': str(result2['ApiToken']),
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'api.pxb7.com',
            'LoginStatus': 'false',
            'Origin': 'https://www.pxb7.com',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'randomStr': str(result2['RandomStr']),
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sign': str(result2['Sign']),
            'timestamp': str(result2['Timestamp']),
            'token': str(result2['token']),
            'Cookie': 'acw_tc=2b8b5799d03c2c7cd85ae7d15587453dbe7bccbae6912614583068b220c2e061; aliyungf_tc=b071b2cb596818a83d137942c3f307ce410e5e02411f63933d5a8e3ee89d8ee6'
        }
        print(headers)
        try:
            response = requests.request("GET", url, headers=headers)
            print(response.text)
            mydict = json.loads(response.text)
            a = mydict['data']['list']
            for tmp in a:
                self.des = tmp['name']
                prebianhao = re.search('^【([A-Z|0-9]+)】', self.des)
                if prebianhao is None:
                    continue
                self.wujiang=str(self.des).split('动态皮肤：')[0]
                self.bianhao = prebianhao.group(1)
                self.price = int(tmp['price'])
                mysearch = "select * from sanguosha where bianhao='{bianhao}'".format(bianhao=self.bianhao)
                self.cursor.execute(mysearch)
                if not len(self.cursor.fetchall()):
                    self.check_and_notify_users()
                    sql = "insert into sanguosha(bianhao,price,des) values('{bianhao}',{price},'{des}') ".format(
                        bianhao=self.bianhao, price=self.price, des=self.des[:500])
                    self.cursor.execute(sql)
                    self.db.commit()
        except  Exception as e:
            print('getpangxiedata:' + e.__str__())

    def clean_expired_users(self):
        try:
            with self.db.cursor() as cursor:
                sql = "DELETE FROM sanguosha_user WHERE expiration_date < CURDATE()"
                cursor.execute(sql)
                self.db.commit()
        except Exception as e:
            traceback.print_exc()
            print(f"Error cleaning expired users: {e}")

if __name__ == '__main__':
    account_checker = AccountChecker()
    while True:
        print(1)
        account_checker.clean_expired_users()
        account_checker.getpanzhidata()
        account_checker.getpangxiedata()
        time.sleep(60)
