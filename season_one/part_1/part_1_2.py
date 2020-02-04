# coding=utf8

import requests
import re


def get_one():
    """
    发起get请求
    :return:
    """
    r = requests.get('')
    print(r.text)


def get_two():
    """
    发起get请求.追加参数
    :return:
    """
    data = dict(name='', age=0)
    r = requests.get('', params=data)
    print(r.text)
    print(r.json())
    print(type(r.json()))


def set_header():
    """
    设置header
    :return:
    """
    
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    headers = {
        'User-Agent': USER_AGENT,
    }
    r = requests.get('https://www.zhihu.com/explore', headers=headers)
    pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
    titles = re.findall(pattern, r.text)
    print(titles)


def get_file_to_save():
    """
    抓取二进制文件保存。图片。音频。视频
    :return:
    """
    url = 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/_images/6.1.jpg'

    r = requests.get(url)
    with open("D://x.jpg", 'wb') as f:
        f.write(r.content)
    print("success")


def post_one():
    """
    发起post请求
    :return:
    """
    data = {"name": '', 'age': 0}
    r = requests.post('', data=data)
    print(r.text)
