# ZhihuSpider
User spider for www.zhihu.com
## 1.Install python3 and packages
Make sure you have installed python3.
Using pip to install dependencies.
``` bash
pip install Image requests beautifulsoup4 html5lib redis PyMySQL 
```
## 2.Database Config
Install `mysql`,create your database.
Import `init.sql` to create your table.

## 3.Install redis
``` bash
# (ubuntu)
apt-get install redis

# or (centos)

yum install redis

# or (macos)
brew install redis
```
## 4.Config your application
Complete config.ini

## 5.Get start
``` bash
python get_user.py

# or command python3

python3 get_user.py
```

## 中文

# 这是一个多线程抓取知乎用户的程序

# Requirements

需要用到的包：
`beautifulsoup4`
`html5lib`
`image`
`requests`
`redis`
`PyMySQL`

pip安装所有依赖包：
``` bash
pip install Image requests beautifulsoup4 html5lib redis PyMySQL 
```

运行环境需要支持中文

测试运行环境python3.5，不保证其他运行环境能完美运行

1.**需要安装mysql和redis**

2.**配置`config.ini`文件，设置好mysql和redis，并且填写你的知乎帐号

可以通过配置`config.ini`文件下的`[sys]` `sleep_time` 控制爬虫速度（尽量使用推荐值，过快容易被知乎封禁），`thread_num`配置线程数目

3.**向数据库导入`init.sql`**

# Run

开始抓取数据:`python get_user.py`
查看抓取数量:`python check_redis.py`
