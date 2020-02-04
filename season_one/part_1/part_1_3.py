# coding=utf8

import requests


def upload_file():
    """
    上传文件
    :return:
    """
    files = {"file": open("../../static_files/image.png", 'rb')}
    r = requests.post("", files=files)
    print(r.text)


def use_cookie_one():
    """
    通过header使用cookie
    :return:
    """
    # cookie的值应使用浏览器登录后适时获取
    # Host应该与访问的网站一致
    # User-Agent应该与登录的浏览器一致
    headers = {
        "Cookie": '',
        "Host": "www.zhihu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    r = requests.get('https://www.zhihu.com/people/ai-bo-11/activities', headers=headers)
    print(r.status_code)
    # 通过查询页面只有登录后才会存在的文字来判断是否伪装登录成功
    print(r.text.find('艾'))


def use_cookie_two():
    """
    使用cookies参数设置cookie
    :return:
    """
    cookies = ''
    jar = requests.cookies.RequestsCookieJar()
    headers = {
        "Host": "www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar.set(key, value)
    r = requests.get('https://www.zhihu.com', cookies=jar, headers=headers)
    # 通过查询页面只有登录后才会存在的文字来判断是否伪装登录成功
    print(r.text.find("几字微言"))
    

def hold_session():
    """
    会话维持,正常情况下两次请求相当于两个不同浏览器打开的两个网页。
    使用session可以让两次请求使用同一个会话信息
    :return:
    """
    s = requests.session()
    # 设置cookie
    s.get('')
    # 读取cookie
    r = s.get('')
    print(r.text)


def use_cookie_two_hold_session():
    """
    会话保持。知乎登录状态伪装
    :return:
    """
    cookies = ''
    jar = requests.cookies.RequestsCookieJar()
    headers = {
        "Host": "www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar.set(key, value)
    s = requests.session()
    s.cookies = jar
    s.headers = headers
    # 访问首页。若有写文章的文字则说明已登录
    r = s.get('https://www.zhihu.com')
    print(r.text.find("写文章"))
    # 再访问个人资料编辑页面。若能访问则说明已登录
    r = s.get('https://www.zhihu.com/people/edit')
    print(r.text.find('茅十八'))


def ssl_verify():
    """
    对https站点发起请求。
    :return:
    """
    from requests.packages import urllib3
    # 忽略警告
    urllib3.disable_warnings()
    
    # verify=False可以屏蔽系统对ssl的验证。默认为True。若证书不正确会抛出异常
    response = requests.get("https://uu898.com", verify=False)
    print(response.status_code)


def ssl_verify_logging():
    """
    对https站点发起请求。并通过日志的方式忽略警告
    :return:
    """
    import logging
    logging.captureWarnings(True)
    response = requests.get("https://uu898.com", verify=False)
    print(response.status_code)


def proxy_set():
    """
    使用代理。
    :return:
    """
    proxies = {
        "http": "185.132.133.99:1080",
        # "https": "http://10.10.1.10:1080",
    }
    
    response = requests.get("https://www.taobao.com", proxies=proxies)
    print(response.status_code)


def proxy_set_http_auth():
    """
    使用需要验证Http Base Auth的代理
    :return:
    """
    proxies = {
        'http': 'http://user:password@host:port',
    }
    response = requests.get("http://www.taobao.com", proxies=proxies)
    print(response.status_code)


def proxy_set_socks():
    """
    使用socks协议代理
    需要安装socks库  pip install 'requests[socks]'
    :return:
    """
    proxies = {
        'http': 'socks5://61.129.70.109:1080',
        #'https': 'socks5://user:password@host:port'
    }
    response = requests.get("http://www.taobao.com", proxies=proxies)
    print(response.status_code)


def timeout_set():
    """
    超时设置
    :return:
    """
    r = requests.get('https://www.taobao.com', timeout=1)
    print(r.status_code)


def timeout_set_many():
    """
    分别设置connect阶段的超时时间和read阶段的超时时间
    :return:
    """
    # 5秒连接超时。10秒读取超时， 20秒总时间超时
    r = requests.get('https://www.taobao.com', timeout=(3, 10))
    print(r.status_code)


def base_auth():
    """
    访问需要http base auth验证的网页
    :return:
    """
    from requests.auth import HTTPBasicAuth
    
    r = requests.get('http://localhost:8001', auth=HTTPBasicAuth('username', 'password'))
    print(r.status_code)
    # 默认会使用HTTPBasicAuth方式验证
    r = requests.get('http://localhost:8001', auth=('username', 'password'))
    print(r.status_code)


def oauth_request():
    """
    通过OAuth认证。需要安装  pip3 install requests_oauthlib
    :return:
    """
    from requests_oauthlib import OAuth1
    
    url = 'https://xxxxxx'
    auth = OAuth1('APP_KEY', 'APP_SECRET', 'OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET')
    resposne = requests.get(url, auth=auth)


def prepared_request():
    """
    Prepared Request演示。未发现特殊作用。暂不讲解
    :return:
    """
    from requests import Request, Session
    url = ''
    data = {"name": ''}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    s = Session()
    req = Request('POST', url, data=data, headers=headers)
    prepped = s.prepare_request(req)
    
    r = s.send(prepped)
    print(r.text)
    

if __name__ == "__main__":
    upload_file()
