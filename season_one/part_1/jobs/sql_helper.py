import pymysql

DB_IP = "127.0.0.1"
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = '123456'


class MySqlHelper:
    def __init__(self):
        self.connect = pymysql.Connect(host=DB_IP, port=DB_PORT, user=DB_USER, password=DB_PWD, database='jd_sku')
        cur = self.connect.cursor()
        if not cur:
            raise (NameError, "connect db fail")
        self.cursor = cur

    def exec_query(self, sql, param=None):
        """
        执行查询返回所有符合条件的数据
        :param sql:
        :param param:
        :return:
        """
        if not self.connect.open:
            self.__init__()
        if param is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, param)
        result = self.cursor.fetchall()
        self.connect.close()
        return result

    def exec_no_query(self, sql, param=None):
        """
        单条语句执行
        :param sql: 格式化后的sql语句。若有参数。需要使用占位符
        :param param: 若为None则忽略此参数。否则应为tuple,list,dict
        :return:
        """
        if not self.connect.open:
            self.__init__()
        if param is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, param)
        self.connect.commit()
        self.connect.close()

    def exec_many(self, sql, param_list):
        """
        批量写入。
        :param sql: 格式化的sql语句。参数位置使用占位符%s
        :param param_list: 值列表。列表内元素的类型可为tuple,list,dict
        :return: None
        """
        if not self.connect.open:
            self.__init__()

        self.cursor.executemany(sql, param_list)
        self.connect.commit()
        self.connect.close()


if __name__ == "__main__":
    mysql = MySqlHelper()
    sql = "INSERT INTO jd_item(sku_id, detail_url, list_img_url, title, price) VALUES(%s,%s,%s,%s,%s)"
    # mysql.exec_no_query(sql, ['a1', 'a2', 'a3', 300.23])
    # print("over")
    # value_list = [['100000769466',
    #                '//item.jd.com/100000769466.html',
    #                '//img11.360buyimg.com/n7/jfs/t27163/354/1454412463/213745/cb143ad4/5bc8229fN71106836.jpg',
    #                '联想(Lenovo)拯救者Y7000 15.6英寸游戏笔记本电脑(英特尔八代酷睿i5-8300H 8G 512G SSD GTX1050 黑)',
    #                5699.00]]
    # mysql.exec_many(sql, value_list)
    # print('over')
