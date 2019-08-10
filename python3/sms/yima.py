# -*- coding: UTF-8 -*-
import json
import re
import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Yima():
    def __init__(self, token=None, project_id=None, username=None, password=None, project_name=None):
        self.session = requests.Session()
        self.token = token
        self.project_id = project_id
        self.username = username
        self.password = password
        self.project_name = project_name

    def login(self, username, password):
        retry = 0
        while True:
            retry += 1
            if retry == 10:
                logging.info("retry failed after 10 times, exit")
                raise Exception
            try:
                content = self.session.get(
                    "http://api.fxhyd.cn/UserInterface.aspx?action=login&username={}&password={}". \
                        format(username, password)).text
                logging.info(content)
                if content.find('html') > -1:
                    # print('cookie已过期，请手动登录后重新获得')
                    # print(rUser.url)
                    continue
                self.token = content.split('|')[1]
                break
            except:
                logging.error("retry,continue get token")
                continue

    def get_phone_number(self, project_id=None, token=None):
        if not project_id:
            project_id = self.project_id
        if not token:
            token = self.token
        retry = 0
        while retry < 10:
            retry += 1
            try:
                result = self.session.get(
                    "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&itemid={}&token={}"
                        .format(self.project_id, self.token)).text
            except:
                logging.error("get phone num failed, retry...")
                continue
            try:
                phone_number = result.split('|')[1]
            except:
                logging.error("extract phone num failed, retry...")
                time.sleep(3)
                continue
            return phone_number
        return ''

    def get_origin_message(self, phone_number=None, token=None, project_id=None, phone=None):
        # print(self.token, self.project_id, self.phone_number)
        try:
            result = self.session.get(
                "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&mobile={}&itemid={}&token={}". \
                    format(phone_number, self.project_id, self.token))
            return result.content.decode('utf-8')
        except Exception as e:
            logging.warning(str(e).replace('\n', '\\\n'))

    def generate_phone(self):
        self.login(self.username, self.password)

        phone_number = self.get_phone_number()
        logging.info(phone_number)
        # print(self.get_origin_message())
        return phone_number

    def release_num(self, phone_number=None):
        rls_url = "http://api.fxhyd.cn/UserInterface.aspx?action=release&mobile={}&itemid={}&token={}". \
            format(phone_number, self.project_id, self.token)
        result = self.session.get(rls_url).text
        if result.find('html') > -1:
            # print('cookie已过期，请手动登录后重新获得')
            # print(rms.url)
            raise Exception
        if result.find('success'):
            logging.info('已成功释放手机号:{}'.format(phone_number))
            return True

    def get_message(self, phone=None):
        for _ in range(15):
            time.sleep(5)
            text = self.get_origin_message(phone)
            logging.info("get message:{}".format(text))
            try:
                print('yanzhengmaz;', text)
                m = re.findall(r'验证码为：(\d+)', text)[0]
            except:
                logging.info("extract message failed, retry...")
                continue
            else:
                result = self.release_num(phone)
                return m
        result = self.release_num(phone)
        return None


# 使用 阿布云代理
def get_proxies():
    proxy_host = "http-dyn.abuyun.com"
    proxy_port = "9020"
    proxy_user = "HHH23CH05C3RY94D"
    proxy_pass = "63242ADB7804FEB4"
    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_user,
        "pass": proxy_pass,
    }

    proxies = {
        "http": proxy_meta,
        "https": proxy_meta,
    }
    return proxies


def send_sms(proxies, phone):
    url = "https://android.fuliapps.com/sms/sendv"
    querystring = {"apiVersion": "28", "deviceModel": "COL-AL10", "brand": "HONOR", "deviceName": "HWCOL",
                   "serial": "VBJ4C18504000167", "platform": "android", "version": "3.5.1",
                   "_t": "" + str(int(round(time.time() * 1000))) + ""}
    payload = "mobi=" + phone + "&sendcount=0&mobiprefix=%2B86"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': "okhttp/3.11.0",
        'Accept': "*/*",
        'Host': "android.fuliapps.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "45",
        'Connection': "keep-alive"
    }

    response = requests.request("POST", url, proxies=proxies, data=payload, headers=headers, params=querystring)

    logging.info(response.status_code)
    logging.info(json.loads(response.text))
    if response.status_code != 200:
        return False
    return True


def register(proxies, phone, msg):
    url = "https://android.fuliapps.com/register"

    querystring = {"apiVersion": "28", "deviceModel": "COL-AL10", "brand": "HONOR", "deviceName": "HWCOL",
                   "serial": "VBJ4C18504000167", "platform": "android", "version": "3.5.1",
                   "_t": "" + str(int(round(time.time() * 1000))) + ""}

    payload = "password=123456789&gender=1&smscode=" + msg + "&invitecode=VNBGGY&mobi=" + phone + "&mobiprefix=%2B86&aup=1"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': "okhttp/3.11.0",
        'Accept': "*/*",
        'Host': "android.fuliapps.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "100",
        'Connection': "keep-alive"
    }

    response = requests.request("POST", url, proxies=proxies, data=payload, headers=headers, params=querystring)

    logging.info(response.status_code)
    logging.info(json.loads(response.text))


def main():
    yima = Yima(username="Ywainli", password="gm5PZffFP7cjDJP", project_id=33506, project_name=u"香蕉视频")
    phone = yima.generate_phone()
    logging.info("phone=" + phone)
    # logging.info('{phone} --> {message}'.format(phone=xunma.generate_phone(), message=xunma.get_message()))
    proxies = get_proxies()
    send_sms(proxies, phone)
    msg = yima.get_message(phone)
    logging.info("验证码=" + msg)
    register(proxies, phone, msg)
    yima.release_num(phone)


if __name__ == '__main__':
    for i in range(11):
        print("--------第" + str(i) + "次")
        main()

        time.sleep(10)
