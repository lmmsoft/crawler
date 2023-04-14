# 欢迎阅读 《MacOS上使用Charles抓包，再用 ChatGPT 写爬虫抢票》 https://lmmsoft.github.io/charles_crawler/ 这是参考代码

import datetime
import time

import requests


def crawler():
    date_to_str = {
        "2023-04-14": "周五",
        "2023-04-15": "周六",
        "2023-04-16": "周日",
    }
    headers = {
        "Host": "ws.taoart.com",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ws.taoart.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.7(0x13070010) Safari/605.1.15 NetType/WIFI",
        "Referer": "https://ws.taoart.com/ticket/buy-ticket.htm?informationId=1279&*******",
        "Sec-Fetch-Dest": "empty",
        "Cookie": "********"
    }

    url = "https://ws.taoart.com/ticket/ajax-time.htm"

    while True:
        for k, v in date_to_str.items():
            data = {
                "informationId": "1279",
                "ticketId": "12595",
                "planType": "1",
                "viewDate": {k},
            }

            flag_found = False
            response = requests.post(url, headers=headers, data=data)
            js_dict = response.json()

            exports = js_dict['exports']
            for export in exports:
                if export['surplus'] != '余量:0':
                    pub_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    hint = f"{k} {v}的票已经出来啦！{export['name']}-{export['surplus']}，赶紧去抢票! 信息发布时间{pub_time}， 一般一分钟内能抢到！"
                    send_ding_message(hint)
                    print(hint)
                    flag_found = True

            if not flag_found:
                print(f"{k} {v} 没找到票，继续等待... {datetime.datetime.now()}")

            time.sleep(60)

        time.sleep(120)


def send_ding_message(text):
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=******"

    # 构造请求数据
    data = {
        "msgtype": "text",
        "text": {
            "content": f"hi ：{text}"
        },
        "at": {
            "isAtAll": True,
        }
    }

    # 发送POST请求到钉钉机器人API
    response = requests.post(webhook_url, json=data)

    # 输出请求结果
    print(response.text)


if __name__ == '__main__':
    send_ding_message("开始抢票啦！")
    crawler()
