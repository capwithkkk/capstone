import pymysql


class insert:
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost',
                               user = 'admin',
                               password = 'admin',
                               db = 'capstone',
                               charset = 'utf8')
        self.curs = self.conn.cursor()

    def make_insert_query(self,name,store,url,pic_url,price):
        try:
            sql = 'INSERT INTO product VALUES(null,"'+name+'","'+ store +'","'+url+'","' + pic_url + '",'+str(price).replace(",","")+',null,1)'
            print(sql)
            self.curs.execute(sql)


            sql2 = 'select * from product'
            self.curs.execute(sql2)
            self.conn.commit()
        except pymysql.err.IntegrityError:
            pass

    def take_query(self,sql):
        try:
            self.curs.execute(sql)
            return self.curs.fetchall()
        except pymysql.err.IntegrityError:
            pass

    def on_destroy(self):
        self.conn.close()
