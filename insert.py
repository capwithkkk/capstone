import pymysql

class insert:
    def __init__(self):
        pass

    def make_insert_query(self,name,store,url,pic_url,price):
        conn = pymysql.connect(host = 'localhost',
                       user = 'root',
                       password = 'root',
                       db = 'capstone',
                       charset = 'utf8')
        curs = conn.cursor()
        sql = 'INSERT INTO product VALUES(null,"'+name+'","'+ store +'","'+url+'","' + pic_url + '",'+price+',null,1)'
        curs.execute(sql)


        sql2 = 'select * from product'
        curs.execute(sql2)
        conn.commit()


        conn.close()

# product 구조 = (pro_index(auto_increment),name,store,url,pic_url,price,expired,category_id)
# test
# name = '"한양"'
# store = '"ABC마트"'
# url = '"www.hanyang.ac.kr"'
# pic_url = '"portal.hanyang.ac.kr"'
# price = "10000"
# 카테고리 자동 분류도 필요하다?  우선 1번 - '전체'
# INSERT INTO product VALUES(null,name,store,url,pic_url,price,null,3);




i = insert();

# i.make_insert_query('한양','ABC마트','www.hanyang.ac.kr','portal.hanyang.ac.kr',"10000")
