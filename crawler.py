import abc, time
from repeater import Repeater
from insert import Database
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from singleton import SingletonInstance
import xml.etree.ElementTree as ElementTree
import requests


class ParserUnit:

    def __init__(self, store):
        self.store = store
        self.rules = self.get_parse_rule()
        for rule in self.rules:
            self.search = rule[0]
            self.section = rule[1]
            self.articles = rule[2]
            self.name = rule[3]
            self.url = rule[4]
            self.pic_url = rule[5]
            self.price = rule[6]
            self.button = rule[7]
        #self.extra_rules = self.get_parse_rule_extra()
        #for rule in self.extra_rules:
        #    self.category = rule[0]
        #    self.brand = rule[1]
        #    self.in_link = rule[2]

    def get_parse_rule(self):
        return Database.instance().take_query("SELECT search,section,articles,name,url,pic_url,price,button FROM parse_rule WHERE store = '" + self.store  + "'")

    def get_parse_rule_extra(self):
        return Database.instance().take_query("SELECT category,brand,is_inlink FROM parse_rule WHERE store = '" + self.store  + "'")


class Data:

    def __init__(self, name, url, pic_url, price, category):
        self.name = name
        self.url = url
        self.pic_url = pic_url
        self.price = price
        self.category = category


class CategoryDict(SingletonInstance):

    def __init__(self):
        self.categories = {}
        category_table = CategoryDict.get_categories()
        for category in category_table:
            self.categories[category[1]] = category[0]

    @staticmethod
    def get_categories():
        return Database.instance().take_query("SELECT category_id, category_name FROM category")


class CategoryConverger(SingletonInstance):

    def __init__(self, name, category):
        self.origin_name = name
        self.rules = CategoryConverger.get_category_converger()
        self.dict = {}
        for rule in self.rules:
            self.dict[rule[0]] = rule[1]

    def substitute_category(self, name):
        if name in self.dict:
            return self.dict[name]
        else:
            print("치환실패 -")
            return "전체"

    @staticmethod
    def get_category_converger():
        return Database.instance().take_query("SELECT * from category_convergence")


class ParserInterface(abc.ABC):

    @abc.abstractclassmethod
    def parse_to_list(self, driver: webdriver) -> Data:
        raise NotImplementedError()


class ParserImpl(ParserInterface):

    def __init__(self,store):
        self.store = store
        self.parser_unit = ParserUnit(store)

    def parse_to_list(self, driver:webdriver) -> []:
        rule_list = []
        try:

            section = driver.find_element_by_xpath(self.parser_unit.section)
            articles = section.find_elements_by_xpath(self.parser_unit.articles)

            for article in articles:
                name0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.name},StaleElementReferenceException,2)
                name = name0.text

                url0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.url},StaleElementReferenceException,2)
                url = url0.get_attribute('href')

                pic_url0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.pic_url},StaleElementReferenceException,2)
                pic_url = pic_url0.get_attribute('src')

                price0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.price},StaleElementReferenceException,2)
                price = price0.text

                print("""
                    name   : %s
                    url    : %s
                    pic_url: %s
                    price  : %s
                    """ % (name, url, pic_url, price)
                      )
                #todo implement
                #if self.parser_unit.in_link:
                #    new_page = None
                #    category = ParserImpl.find_item_info_from_link(url, self.parser_unit.category)
                #    brand = ParserImpl.find_item_info_from_link(url, self.parser_unit.category)
                #else:
                #    category = ParserImpl.find_item_info_from_article(article, self.parser_unit.category)
                #    brand = ParserImpl.find_item_info_from_article(article, self.parser_unit.category)

                rule_list.append(Data(name, url, pic_url, price, "전체"))
        except NoSuchElementException:
            pass
        return rule_list

    @staticmethod
    def find_item_info_from_article(driver: webdriver, parse_rule: str) -> str:
        return driver.find_element_by_xpath(parse_rule).text

    @staticmethod
    def find_item_info_from_link(url: str, parse_rule: str) -> str:
        req = requests.get(url)
        root = ElementTree.fromstring(req.content)
        elem = root.find(parse_rule)
        return elem.itertext()


class MinerInterface(abc.ABC):

    @abc.abstractclassmethod
    def search_init(self, keyword:str):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def do_next_page(self):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get_store(self) -> str:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get_driver(self) -> webdriver:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get_query_input_element(self) -> webdriver:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get_next_button_element(self) -> webdriver:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def insert_to_db(self, name, url, pic_url, price, category):
        raise NotImplementedError()


class MinerImpl(MinerInterface):

    def __init__(self, driver, store, url, parser):
        self.store = store
        self.url = url
        if parser is None and store is not None:
            self.parser = MinerImpl.get_parser(self.store)
        else:
            self.parser = parser
        if driver is None:
            self.driver = MinerImpl.create_driver()
        else:
            self.driver = driver

    @staticmethod
    def create_driver() -> webdriver:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        option.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(chrome_options=option,executable_path="./chrome/chromedriver")

    @staticmethod
    def get_parser(store:str) -> ParserInterface:
        return ParserImpl(store)

    def get_store(self) -> str:
        return self.store

    def get_driver(self) -> webdriver:
        return self.driver

    def set_store(self, store, url, parser):
        self.store = store
        self.url = url
        self.parser = parser

    def search_init(self,keyword:str):
        driver_element = self.get_query_input_element()
        driver_element.send_keys(keyword)
        driver_element.submit()

    def do_next_page(self) -> bool:
        page_element = self.get_next_button_element()
        if page_element is None:
            return False
        self.driver.execute_script("arguments[0].click()", page_element)
        return True

    def get_query_input_element(self) -> webdriver:
        return self.driver.find_element_by_xpath(self.parser.parser_unit.search)

    def get_next_button_element(self) -> webdriver:
        try:
            return self.driver.find_element_by_xpath(self.parser.parser_unit.button)
        except NoSuchElementException:
            return None

    def insert_to_db(self, name, url, pic_url, price, category):
        Database.instance().make_insert_query(name, self.store, url, pic_url, price, category)

    def mining(self, keyword):
        driver = self.driver
        driver.get(self.url)
        self.search_init(keyword)
        front_item_name = ""
        page = 1
        while True:
            try:
                print("page : " + str(page))
                data_list = self.parser.parse_to_list(self.driver)
                if len(data_list) == 0 or front_item_name == data_list[0].name:
                    print("사유 : " + str(len(data_list)))
                    break
                else:
                    front_item_name = data_list[0].name
                '''
                for data in data_list:
                    print("""
                    name   : %s
                    store  : %s
                    url    : %s
                    pic_url: %s
                    price  : %s
                    category_num : %s
                    """ % (data.name, self.store, data.url, data.pic_url, data.price, CategoryDict.instance().categories[data.category]))
                '''
                    #Database.instance().insert_to_db(data.name, data.url, data.pic_url, data.price, CategoryDict.instance().categories[data.category])
                if not self.do_next_page():
                    break
                page += 1
            except StaleElementReferenceException:
                time.sleep(0.1)



miner = MinerImpl(None, "11번가", "http://www.11st.co.kr/", None)
miner.mining("신발")
