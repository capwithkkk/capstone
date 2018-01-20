from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from insert import insert
import time

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

        option = webdriver.ChromeOptions()
        #option.add_argument('headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        #prefs = {"profile.managed_default_content_settings.stylesheets":2}
        option.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(chrome_options=option,executable_path="./chrome/chromedriver")

        driver.get(url)
        driver_element = driver.find_element_by_id("AKCKwd")
        driver_element.send_keys(query)
        driver_element.submit()

        while count >0:
            print("count : " +str(count))

            section = driver.find_elements_by_css_selector("div.normal_prd")[0]

            articles = section.find_elements_by_css_selector("div.total_listing_wrap > ul.tt_listbox li[id^='thisClick_']")
            for article in articles:
                name = article.find_elements_by_css_selector("p.info_tit")[0].find_element_by_tag_name("a").text
                url  = article.find_elements_by_css_selector("p.info_tit")[0].find_element_by_tag_name("a").get_attribute('href')
                pic_url = article.find_elements_by_css_selector("div.photo_wrap > a")[0].find_element_by_tag_name("img").get_attribute('data-original')
                price = article.find_elements_by_css_selector("span.price_detail")[0].find_element_by_tag_name("strong").text

                print("""
                name   : %s
                store  : %s
                url    : %s
                pic_url: %s
                price  : %s
                """ % (name,store,url,pic_url,price))
                #insert.make_insert_query(name,store,url,pic_url,price)
            print("target : " + str(page_num+1))

            element = driver.find_elements_by_css_selector("div#list_paging > span a")[0]

            driver.execute_script("arguments[0].click()",element)
            time.sleep(1)

            count -= 1
            page_num += 1


    #G마켓 테스트용
    def httpGet2(self,url,query,store,count):

        page_num = 1

        print("start with : " + url)

        option = webdriver.ChromeOptions()
        #option.add_argument('headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        #prefs = {"profile.managed_default_content_settings.stylesheets":2}
        option.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(chrome_options=option,executable_path="./chrome/chromedriver")

        driver.get(url)
        driver_element = driver.find_element_by_id("keyword")
        driver_element.send_keys(query)
        driver_element.submit()

        while count >0:
            print("count : " +str(count))
            #print(driver.page_source)
            #soup = BeautifulSoup(driver.page_source,'html.parser')


            section = driver.find_elements_by_css_selector("ul#searchListItems")[0]
            articles = section.find_elements_by_css_selector("li.focusitem")
            for article in articles:
                name = article.find_elements_by_css_selector("span.title")[0].text
                url  = article.find_elements_by_css_selector("div.item_info")[0].find_element_by_tag_name("a").get_attribute('href')
                pic_url = article.find_elements_by_css_selector("span.thumb")[0].find_element_by_tag_name("img").get_attribute('src')
                price = article.find_elements_by_css_selector("span.price a")[0].find_element_by_tag_name("strong").text

                print("""
                name   : %s
                store  : %s
                url    : %s
                pic_url: %s
                price  : %s
                """ % (name,store,url,pic_url,price))
                #insert.make_insert_query(name,store,url,pic_url,price)
            print("target : " + str(page_num+1))

            element = driver.find_element_by_css_selector("div.paginate > span.button_next > a")

            driver.execute_script("arguments[0].click()",element)
            time.sleep(1)

            count -= 1
            page_num += 1
            time.sleep(2)
        time.sleep(300)


    #옥션 테스트용
    def httpGet3(self,url,query,store,count):

        page_num = 1

        print("start with : " + url)
        driver = webdriver.Chrome("./chrome/chromedriver")

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

            element = driver.find_element_by_css_selector("div.paginate > span.nxt")
            driver.execute_script("arguments[0].click()",element)
            time.sleep(1)

            count -= 1
            page_num += 1






t = TestModule();


#t.httpGet0("http://emart.ssg.com/search.ssg?target=all&query=호버보드&page=","","이마트몰",1,2)
#t.httpGet1("http://www.11st.co.kr/html/main.html","호버보드","11번가",1)
#t.httpGet2("http://www.gmarket.co.kr/","접시","G마켓",1)
#t.httpGet3("http://www.auction.co.kr/","호버보드","옥션",1)

print("abc");
