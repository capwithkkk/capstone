from bs4 import BeautifulSoup
import requests

class TestModule:

    def __init__(self):
        pass

    def checkType(self,param):
        print("param check : " + str(type(param)))


    def httpGet(self,str_init,str_end,store,start,end):
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

            #section : (tbody#itemList)
            #article : (tr#item_unit_*)
                #name :





t = TestModule();

t.httpGet("http://emart.ssg.com/search.ssg?target=all&query=쌀&page=","","이마트몰",1,2)
