# -*- coding: utf-8 -*-
import sys
from login.login import Login as Login
import requests
import http.cookiejar as cookielib
import configparser
from bs4 import BeautifulSoup
import redis
import json
import math
import pymysql
import traceback
import threading
import time
import random

# 获取配置
cfg = configparser.ConfigParser()
cfg.read("config.ini")

class GetUser(threading.Thread):
    session = None
    config = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "Origin": "https://www.zhihu.com/",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/json, text/plain, */*",
        "Pragma": "no-cache",
        "Accept-Encoding": "gzip, deflate",
        'Connection': 'close',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    retry = 0  # 重试次数
    redis_con = ''
    counter = 0  # 被抓取用户计数
    xsrf = ''
    db = None
    db_cursor = None
    max_queue_len = 1000  # redis带抓取用户队列最大长度
    ua = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    )
    sleep_time = 1

    def __init__(self, threadID=1, name=''):
        # 多线程
        print("线程" + str(threadID) + "初始化")
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        try:
            print("线程" + str(threadID) + "初始化成功")
        except Exception as err:
            print(err)
            print("线程" + str(threadID) + "开启失败")

        self.threadLock = threading.Lock()

        # 获取配置
        self.config = cfg

        # 初始化session
        requests.adapters.DEFAULT_RETRIES = 5
        self.session = requests.Session()
        self.session.cookies = cookielib.LWPCookieJar(filename='cookie')
        self.session.keep_alive = False
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print('Cookie 未能加载')
        finally:
            pass

        # 创建login对象
        
        # lo = Login(self.session)
        # lo.do_login()
        

        # 初始化redis连接
        try:
            redis_host = self.config.get("redis", "host")
            redis_port = self.config.get("redis", "port")
            self.redis_con = redis.Redis(host=redis_host, port=redis_port, db=0)
            # 刷新redis库
            # self.redis_con.flushdb()
        except Exception as err:
            print("请安装redis或检查redis连接配置")
            sys.exit()

        # 初始化数据库连接
        try:
            db_host = self.config.get("db", "host")
            db_port = int(self.config.get("db", "port"))
            db_user = self.config.get("db", "user")
            db_pass = self.config.get("db", "password")
            db_db = self.config.get("db", "db")
            db_charset = self.config.get("db", "charset")
            self.db = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pass, db=db_db,
                                      charset=db_charset)
            self.db_cursor = self.db.cursor()
        except Exception as err:
            print("请检查数据库配置")
            sys.exit()

        # 初始化系统设置
        self.max_queue_len = int(self.config.get("sys", "max_queue_len"))
        self.sleep_time = float(self.config.get("sys", "sleep_time"))

    # 获取问答html
    def get_index_page(self):
        index_url = 'https://www.zhihu.com/question/waiting'
        try:
            index_html = self.session.get(index_url, headers=self.headers, timeout=35)
        except Exception as err:
            # 出现异常重试
            print("获取页面失败，正在重试......")
            print(err)
            traceback.print_exc()
            return None
        finally:
            self.save_cookie()
            pass
        return index_html.text

    # 获取问题列表，存入redis
    def get_index_page_question(self):
        index_html = self.get_index_page()
        if not index_html:
            return
        BS = BeautifulSoup(index_html, "html.parser")
        # 获取用户的a标签
        question_a = BS.find_all("a", class_="ListQuestionItem-title QuestionWaiting-questionItemTitle ListQuestionItem-title--noDetail")  
        for a in question_a:
            if a:
                href = a.get('href')
                self.add_wait_question(href[(href.rindex('/')) + 1:])
            else:
                print("获取首页author-link失败，跳过")

if __name__ == '__main__':
    # master代码不再需要登陆
    # login = GetUser(999, "登陆线程")

    threads = []
    threads_num = int(cfg.get("sys", "thread_num"))
    for i in range(0, threads_num):
        m = GetUser(i, "thread" + str(i))
        threads.append(m)

    for i in range(0, threads_num):
        threads[i].start()

    for i in range(0, threads_num):
        threads[i].join()