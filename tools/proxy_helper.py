# coding=utf8
"""
处理关于代理ip的问题
"""
import requests


def get_proxy():
    """
    获取代理ip，返回参数字典
    :return:
    """
    response = requests.get("https://dev.kdlapi.com/api/getproxy/?orderid=904547214009772&num=2&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sep=%2C")
    if response.status_code == 200:
        ip_list = response.text.split(',')
    
    return dict(http=ip_list[0], https=ip_list[1])


if __name__ == "__main__":
    get_proxy()