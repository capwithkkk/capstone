import pymysql
import datetime
from singleton import SingletonInstance


class Database(SingletonInstance):

    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost',
                               user = 'admin',
                               password = 'admin',
                               db = 'capstone',
                               charset = 'utf8')
        self.curs = self.conn.cursor()

    def make_query(self, sql):
        try:
            print(sql)
            self.curs.execute(sql)
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print("INTEGRITY 에러 감지")
            pass

    def make_insert_query(self, name, store, url, pic_url, price, category, brand):
        time = datetime.datetime.now()
        nowdays = time + datetime.timedelta(days=30)
        nowdays_str = nowdays.strftime('%Y-%m-%d')
        try:
            sql = 'REPLACE INTO product VALUES(null,"' + str(name) + '","' + str(store) + '","' + str(url) + '","' + str(pic_url) + '",' + str(price).replace(",", "") + ',"' + str(nowdays_str) + '",' + str(category) + ',"' + str(brand) + '")'

            print(sql)
            self.curs.execute(sql)
            self.conn.commit()
        except pymysql.err.IntegrityError:
            sql = 'DELETE FROM product WHERE name = ' + "'" + name + "'"
            self.curs.execute(sql)
            self.conn.commit()
            self.make_insert_query(name, store, url, pic_url, price)

    def take_query(self, sql):
        try:
            self.curs.execute(sql)
            return self.curs.fetchall()
        except pymysql.err.IntegrityError:
            pass

    def take_exe(self,sql):
        try:
            self.curs.execute(sql)
            self.conn.commit()
        except pymysql.err.IntegrityError:
            pass

    def on_destroy(self):
        self.conn.close()
