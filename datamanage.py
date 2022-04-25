import pymysql
import threading
from setting import MYSQL_HOST, MYSQL_DB, MYSQL_PWD, MYSQL_USER


class DataManager():
    # 单例模式，确保每次实例化都调用一个对象。
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DataManager, "_instance"):
            with DataManager._instance_lock:
                DataManager._instance = object.__new__(cls)
                return DataManager._instance

        return DataManager._instance

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PWD, database=MYSQL_DB,
                                    charset='utf8')

        # 建立游标
        self.cursor = self.conn.cursor()
        self.cursor.execute('truncate table douban_movie_250')

    def save_data(self, data):
        sql = 'insert into douban_movie_250(name,mark,comment,year,type,quote,area) values(%s,%s,%s,%s,%s,%s,%s) '
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print('插入数据失败', e)
            self.conn.rollback()  # 回滚

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
