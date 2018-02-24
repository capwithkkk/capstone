import abc
import time
from repeater import Repeater
from insert import Database
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from singleton import SingletonInstance
import lxml.html as lhtml
from lxml.html import HtmlElement
from log import SubstitutionTrialWriter


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
            self.name_attr = rule[8]
            self.url_attr = rule[9]
            self.pic_url_attr = rule[10]
            self.price_attr = rule[11]
        self.extra_rules = self.get_parse_rule_extra()
        for rule in self.extra_rules:
            self.categories = rule[0]
            self.category_core = rule[1]
            self.brand = rule[2]
            self.in_link = rule[3]

    def get_parse_rule(self):
        return Database.instance().take_query(
            "SELECT search,section,articles,name,url,pic_url,price,button,name_attr,url_attr,pic_url_attr,price_attr "
            "FROM parse_rule WHERE store = '" + self.store + "'"
        )

    def get_parse_rule_extra(self):
        return Database.instance().take_query(
            "SELECT categories,category_core,brand,is_inlink FROM parse_rule_extra WHERE store = '" + self.store + "'"
        )


class Data:

    def __init__(self, name, url, pic_url, price, category, brand):
        self.name = name
        self.url = url
        self.pic_url = pic_url
        self.price = price
        self.category = category
        self.brand = brand


class CategoryDict(SingletonInstance):

    def __init__(self):
        self.categories = {}
        self.unclassified_categories = []
        category_table = CategoryDict.get_categories()
        unclassified_category_table = CategoryDict.get_unclassified_categories()
        for category in category_table:
            self.categories[category[1]] = category[0]
        for category in unclassified_category_table:
            self.unclassified_categories.append(category[0])

    @staticmethod
    def get_categories():
        return Database.instance().take_query("SELECT category_id, category_name FROM category")

    @staticmethod
    def get_unclassified_categories():
        return Database.instance().take_query("SELECT category_name FROM category WHERE parent_name = '미분류'")


class CategoryConverger(SingletonInstance):

    def __init__(self):
        self.rules = CategoryConverger.get_category_converger()
        self.dict = {}
        for rule in self.rules:
            self.dict[rule[0]] = rule[1]

    def substitute_category(self, name):
        if name in self.dict:
            return self.dict[name]
        else:
            return None

    @staticmethod
    def get_category_converger():
        return Database.instance().take_query("SELECT * from category_convergence")


class ParserInterface(abc.ABC):

    @abc.abstractclassmethod
    def parse_to_list(self, driver: webdriver) -> Data:
        raise NotImplementedError()


class ParserImpl(ParserInterface):

    def __init__(self, store):
        self.store = store
        self.parser_unit = ParserUnit(store)

    @staticmethod
    def determine_attr_val(driver: webdriver, attr):
        if attr is None:
            return driver.text
        else:
            return driver.get_attribute(attr)

    def parse_to_list(self, driver: webdriver) -> []:
        rule_list = []
        try:

            section = driver.find_element_by_xpath(self.parser_unit.section)
            articles = section.find_elements_by_xpath(self.parser_unit.articles)

            for article in articles:
                name0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.name},StaleElementReferenceException,2)
                name = ParserImpl.determine_attr_val(name0, self.parser_unit.name_attr)

                url0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.url},StaleElementReferenceException,2)
                url = ParserImpl.determine_attr_val(url0, self.parser_unit.url_attr)

                pic_url0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.pic_url},StaleElementReferenceException,2)
                pic_url = ParserImpl.determine_attr_val(pic_url0, self.parser_unit.pic_url_attr)

                price0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.price},StaleElementReferenceException,2)
                price =  ParserImpl.determine_attr_val(price0, self.parser_unit.price_attr)

                if self.parser_unit.in_link:
                    #root = lhtml.fromstring(requests.get(url).text)
                    root = DriverHelper.instance().get_driver()
                    root.get(url)
                    category = ParserImpl.find_category_info(
                        root, self.parser_unit.categories, self.parser_unit.category_core
                    )
                    brand = ParserImpl.find_item_info(root, self.parser_unit.brand)
                else:
                    category = ParserImpl.find_category_info(
                        article, self.parser_unit.categories, self.parser_unit.category_core
                    )
                    brand = ParserImpl.find_item_info(article, self.parser_unit.brand)
                if brand is None or brand is "" or brand in "상품상세설명 참조":
                    brand = "N/A"

                print("""
                    name    : %s
                    url     : %s
                    pic_url : %s
                    price   : %s
                    category: %s
                    brand   : %s
                    """ % (name, url, pic_url, price, category, brand)
                      )

                rule_list.append(Data(name, url, pic_url, price, category, brand))
        except NoSuchElementException:
            pass
        return rule_list

    @staticmethod
    def find_item_info(driver: webdriver, parse_rule: str) -> str:
        try:
            elem = ParserImpl.out_from_xpath(driver, parse_rule)
            text = elem[0].text
            text = text.strip("()[]{} \r\n")
            return text
        except IndexError:
            return "N/A"

    @staticmethod
    def find_category_info(driver: webdriver, categories: str, category_unit: str):
        loaded_categories = ParserImpl.out_from_xpath(driver, categories)
        empty_sub_category_name = "미분류"
        for i in range(len(loaded_categories)-1, -1, -1):
            loaded_category_units = ParserImpl.out_from_xpath(loaded_categories[i], category_unit)
            category = loaded_category_units[0].text.strip("()[]{} \r\n")
            if category is not "전체" and category in CategoryDict.instance().categories:
                return category
            else:
                sub_category = CategoryConverger.instance().substitute_category(category)
                if sub_category is not None:
                    return sub_category
                empty_sub_category_name += " << " + category
                print("치환시도 : " + category)
                SubstitutionTrialWriter.instance().append(category)
        print("미분류 처리 : " + empty_sub_category_name)
        if empty_sub_category_name not in CategoryDict.instance().unclassified_categories:
            print("미분류 소거식 추가")
            CategoryDict.instance().unclassified_categories.append(empty_sub_category_name)
            Database.instance().make_query('INSERT INTO category VALUES(null,"' + empty_sub_category_name + '", "미분류")')
        return empty_sub_category_name

    @staticmethod
    def out_from_xpath(root, xpath: str):
        if isinstance(root, WebElement) or isinstance(root, WebDriver):
            return root.find_elements_by_xpath(xpath)
        elif isinstance(root, HtmlElement):
            return root.xpath(xpath)
        return None


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


class DriverHelper(SingletonInstance):

    def __init__(self):
        self.driver = MinerImpl.create_driver()

    def get_driver(self):
        return self.driver


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
        option.add_argument("--disable-extensions")
        prefs = {"profile.managed_default_content_settings.images":2}
        option.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(chrome_options=option, executable_path="./chrome/chromedriver")

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
        page_parsing_flag = False
        while True:
            try:
                print("page : " + str(page))
                data_list = self.parser.parse_to_list(self.driver)
                if (not page_parsing_flag) and len(data_list) == 0 or front_item_name == data_list[0].name:
                    print("Crawling has been finished.")
                    break
                else:
                    front_item_name = data_list[0].name
                    page_parsing_flag = True
                    for data in data_list:
                        try:
                            Database.instance().make_insert_query(data.name, self.store, data.url, data.pic_url, data.price, CategoryDict.instance().categories[data.category], data.brand)
                        except KeyError:
                            pass
                if not self.do_next_page():
                    break
                page += 1
                page_parsing_flag = False
            except StaleElementReferenceException:
                time.sleep(0.1)


#miner = MinerImpl(None, "옥션", "http://www.auction.co.kr", None)
#miner.mining("테팔")
