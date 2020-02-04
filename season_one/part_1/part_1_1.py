# coding=utf8

import urllib.request
import urllib.parse
import socket


def urlopen_one():
    """
    urlopen使用1
    :return:
    """
    response = urllib.request.urlopen('http://docs.python-requests.org/zh_CN/latest/user/quickstart.html')
    print(response.read().decode('utf-8'))


def urlopen_two():
    """
    urlopen使用2,post数据
    :return:
    """
    data = {"userid": ""}
    # post数据需要把dict转为bytes
    data_bytes = bytes(urllib.parse.urlencode(data), encoding='utf8')
    response = urllib.request.urlopen('', data=data_bytes)
    print(response.code)
    print(response.url)
    print(response.read().decode('utf-8'))


def urlopen_three():
    """
    设置超时时间
    :return:
    """
    
    # 由于没有站点能够达到0.1秒就返回结果的速度。所以这条语句必定抛出time out的异常
    try:
        response = urllib.request.urlopen('', timeout=0.1)

    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print("TIME OUT")


def request_one():
    """
    使用request
    :return:
    """
    request = urllib.request.Request('')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf8'))


def request_two():
    """
    使用request的各种参数
    :return:
    """
    url = ''
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36,
        'Host': ''}
    data = dict(a=1, b='')
    data_bytes = bytes(parse.urlencode(data), encoding='utf8')
    req = urllib.request.Request(url=url, data=data_bytes, headers=headers, method='POST')
    # 若接收请求的url并不支持post方式的请求。则这里可能会抛出405,Not Allowed异常
    response = urllib.request.urlopen(req)
    print(response.read().decode("utf-8"))


def request_two_header():
    """
    request参数设置。header
    :return:
    """
    url = ''
    
    data = dict(a=1, b='')
    data_bytes = bytes(parse.urlencode(data), encoding='utf8')
    req = urllib.request.Request(url=url, data=data_bytes, method='POST')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    req.add_header('Host', '')
    # 若接收请求的url并不支持post方式的请求。则这里可能会抛出405,Not Allowed异常
    response = urllib.request.urlopen(req)
    print(response.read().decode("utf-8"))
