from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from insert import insert

driver = webdriver.PhantomJS("./phantomjs/bin/phantomjs")

class TestModule:

    def __init__(self):
        pass

    def checkType(self,param):
        print("param check : " + str(type(param)))

    #이마트몰 테스트용
    def httpGet0(self,str_init,str_end,store,start,end):
        for i in range(start,end):
            url = str_init + str(i) +str_end
            print("start with : " + url)
            req = requests.get(url)
            self.checkType(req)
            soup = BeautifulSoup(req.content,'html.parser')
            self.checkType(soup)
            section = soup.select("tbody#itemList")[0]
            articles = section.select("tr[id^='item_unit_']")
            for article in articles:
                name = article.select("td:nth-of-type(2) > div > div.item_info")[0].find("a")['title']
                url  = article.select("td:nth-of-type(2) > div > div.item_info")[0].find("a")['href']
                pic_url = article.select("td:nth-of-type(2) > div > div.item_thm > div.thm > a")[0].find("img")['src']
                price = article.select("td:nth-of-type(3) > div.price")[0].find("strong").text

                print("""
            name   : %s
            store  : %s
            url    : %s
            pic_url: %s
            price  : %s
            """ % (name,store,url,pic_url,price))
                insert.make_insert_query(name,store,url,pic_url,price)


    #11번가 테스트용
    def httpGet1(self,url,query,store,count):

        page_num = 1

        print("start with : " + url)
        driver = webdriver.PhantomJS("./phantomjs/bin/phantomjs")
        driver.get(url)
        driver_element = driver.find_element_by_class_name("header_inp_txt")
        driver_element.send_keys(query)
        driver_element.submit()

        while count >0:
            print("count : " +str(count))
            soup = BeautifulSoup(driver.page_source,'html.parser')

            section = soup.select("div.plus_prd")[0]

            articles = section.select("div.total_listing_wrap > ul.tt_listbox li[id^='thisClick_']")
            for article in articles:
                name = article.select("p.info_tit")[0].find("a").text
                url  = article.select("p.info_tit")[0].find("a")['href']
                pic_url = article.select("div.photo_wrap > a")[0].find("img")['data-original']
                price = article.select("span.price_detail")[0].find("strong").text

                print("""
                name   : %s
                store  : %s
                url    : %s
                pic_url: %s
                price  : %s
                """ % (name,store,url,pic_url,price))
                insert.make_insert_query(name,store,url,pic_url,price)
            print("target : " + str(page_num+1))
            driver.find_elements_by_css_selector("div#list_paging > span a")[page_num+1 % 10].click()
            count -= 1
            page_num += 1


    #G마켓 테스트용
    def httpGet2(self,url,query,store,count):

        page_num = 1

        print("start with : " + url)
        driver = webdriver.PhantomJS("./phantomjs/bin/phantomjs")
        driver.get(url)
        driver_element = driver.find_element_by_class_name("sch")
        driver_element.send_keys(query)
        driver_element.submit()

        while count >0:
            print("count : " +str(count))
            soup = BeautifulSoup(driver.page_source,'html.parser')

            section = soup.select("ul#searchListItems")[0]

            articles = section.select("li.plusitem,li.smiledeliveryitem,li.generalitem")
            for article in articles:
                name = article.select("span.title")[0].text
                url  = article.select("div.item_info")[0].find("a")['href']
                pic_url = article.select("span.thumb")[0].find("img")['src']
                price = article.select("span.price a")[0].find("strong").text

                print("""
                name   : %s
                store  : %s
                url    : %s
                pic_url: %s
                price  : %s
                """ % (name,store,url,pic_url,price))
                insert.make_insert_query(name,store,url,pic_url,price)
            print("target : " + str(page_num+1))
            driver.find_element_by_css_selector("div.paginate > span.button_next").click()
            count -= 1
            page_num += 1


    #옥션 테스트용
    def httpGet3(self,url,query,store,count):

        page_num = 1

        print("start with : " + url)
        driver = webdriver.PhantomJS("./phantomjs/bin/phantomjs")
        driver.get(url)
        driver_element = driver.find_element_by_class_name("search_input_keyword")
        driver_element.send_keys(query)
        driver_element.submit()

        while count >0:
            print("count : " +str(count))
            soup = BeautifulSoup(driver.page_source,'html.parser')

            section = soup.select("div#ucItemList_listview, div.list_wrap")[0]

            articles = section.select("div.list_view")
            for article in articles:
                name = article.select("div.item_title")[0].find("a").text.strip()
                url  = article.select("div.item_title")[0].find("a")['href']
                pic_url = article.select("div.image > a")[0].find("img")['data-original']
                price = article.select("div.item_price")[0].find("strong").text



                print("""
                name   : %s
                store  : %s
                url    : %s
                pic_url: %s
                price  : %s
                """ % (name,store,url,pic_url,price))
                insert.make_insert_query(name,store,url,pic_url,price)
            print("target : " + str(page_num+1))
            driver.find_element_by_css_selector("div.paginate > span.nxt").click()
            count -= 1
            page_num += 1






t = TestModule();


t.httpGet0("http://emart.ssg.com/search.ssg?target=all&query=쌀&page=","","이마트몰",1,2)
t.httpGet1("http://www.11st.co.kr/html/main.html","신발","11번가",1)
t.httpGet2("http://www.gmarket.co.kr/","시계","G마켓",1)
t.httpGet3("http://www.auction.co.kr/","프라이팬","옥션",1)

