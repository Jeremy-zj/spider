# coding=utf8
import requests
from bs4 import BeautifulSoup as bs
import json
from sql_helper import MySqlHelper


def read_jd_list(url, item_dict_all=None):
    """
    抓取京东商品三级分类的列表第一页的商品数据。至少包含。标题。详情页地址。价格。列表图片
    :param url:
    :return:
    """

    if item_dict_all is None:
        item_dict_all = dict()
    response = requests.get(url)
    if response.status_code == 200:
        # 使用html.parser解析器对抓取到的html进行解析并格式化为BeautifulSoup对象
        bs_obj = bs(response.text, "html.parser")
        # 分析出页面的商品列表所在容器div的id为plist。则可以针对id对html节点进行过滤。缩小数据查找范围
        # 再从plist中欧查找所有的li。经分析plist中每个li都对应一个商品
        li_list = bs_obj.find(id='plist').find_all('li')

        # 遍历商品列表
        for item in li_list:
            item_dict = dict()
            box = item.find('div')
            sku_id = box.attrs['data-sku']
            link_img = box.find('a')
            detail_url = link_img.attrs['href']
            link_img = link_img.find('img')

            if 'src' in link_img.attrs:
                link_img_url = link_img.attrs['src']
            elif 'data-lazy-img' in link_img.attrs:
                link_img_url = link_img.attrs['data-lazy-img']
            else:
                link_img_url = ""
            name_div = box.select_one('div.p-name')
            title = name_div.find('em').text.strip()
            item_dict['sku_id'] = sku_id
            item_dict['detail_url'] = detail_url
            item_dict['link_img_url'] = link_img_url
            item_dict['title'] = title
            item_dict['price'] = 0
            if sku_id not in item_dict_all:
                item_dict_all[sku_id] = item_dict
    else:
        print("你抓的出问题了！")
    return item_dict_all


def read_item_price(skuid_list, item_dict_all):
    url = "https://p.3.cn/prices/mgets?callback=jQuery7947163&ext=11101000&pin=&type=1&area=1_72_4137_0&skuIds=%s" \
          "&pdbp=0&pdtk=&pdpin=&pduid=15450982118311069858213&source=list_pc_front&_=1545289142553"
    skuids = "%2CJ_".join(skuid_list)
    url = url % skuids
    response = requests.get(url)
    price_str = response.text[response.text.find("["): -3]
    sku_price_list = json.loads(price_str)
    for sku_price in sku_price_list:
        sku_id = sku_price['id'][2:]
        if sku_id in item_dict_all:
            item_dict_all[sku_id]['price'] = float(sku_price['p'])


if __name__ == "__main__":
    url = "https://list.jd.com/list.html?cat=670,671,672"
    item_dict_all = read_jd_list(url)
    skuid_list = [sku for sku in item_dict_all.keys()]
    read_item_price(skuid_list[:30], item_dict_all)
    read_item_price(skuid_list[30:], item_dict_all)

    mysql = MySqlHelper()
    sql = "INSERT INTO jd_item(sku_id, detail_url, list_img_url, title, price) VALUES(%s,%s,%s,%s,%s)"
    values_list = [list(value.values()) for value in item_dict_all.values()]
    mysql.exec_many(sql, values_list)
