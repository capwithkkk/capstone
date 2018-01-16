import abc, time
from insert import insert
from selenium import webdriver


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

    def get_parse_rule(self):
        return insert().take_query("SELECT search,section,articles,name,url,pic_url,price,button FROM parse_rule WHERE store = '" + self.store  + "'")


class Data:
    def __init__(self, name, url, pic_url, price, category):
        self.name = name
        self.url = url
        self.pic_url = pic_url
        self.price = price
        self.category = category

    def get_name(self) -> str:
        return self.name

    def get_url(self) -> str:
        return self.url

    def get_pic_url(self) -> str:
        return self.pic_url

    def get_price(self) -> int:
        return self.price

    def get_category(self) -> str:
        raise self.category


class ParserInterface(abc.ABC):

    @abc.abstractclassmethod
    def parse_to_list(self, driver: webdriver) -> Data:
        raise NotImplementedError()


class ParserImpl(ParserInterface):

    def __init__(self,store):
        self.store = store
        self.parser_unit = ParserUnit(store)

    def parse_to_list(self,driver:webdriver) -> Data:
        rule_list = []
        section = driver.find_element_by_xpath(self.parser_unit.section)
        articles = section.find_elements_by_xpath(self.parser_unit.articles)
        for article in articles:
            name = article.find_element_by_xpath(self.parser_unit.name).text
            url  = article.find_element_by_xpath(self.parser_unit.url).get_attribute('href')
            pic_url = article.find_element_by_xpath(self.parser_unit.pic_url).get_attribute('src')
            price = article.find_element_by_xpath(self.parser_unit.price).text
            rule_list.append(Data(name, url, pic_url, price, "전체"))
        return rule_list


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
        if parser is None:
            self.parser = MinerImpl.get_parser(self.store)
        else:
            self.parser = parser
        if driver is None:
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            prefs = {"profile.managed_default_content_settings.images":2}
            option.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(chrome_options=option,executable_path="./chrome/chromedriver")
        else:
            self.driver = driver

    def get_store(self) -> str:
        return self.store

    def get_driver(self) -> webdriver:
        return self.driver

    def search_init(self,keyword:str):
        driver_element = self.get_query_input_element()
        driver_element.send_keys(keyword)
        driver_element.submit()

    def do_next_page(self) -> bool:
        page_element = self.get_next_button_element()
        if page_element is None:
            return False
        self.driver.execute_script("arguments[0].click()", page_element)
        time.sleep(2)
        return True

    def get_query_input_element(self) -> webdriver:
        return self.driver.find_element_by_xpath(self.parser.parser_unit.search)

    def get_next_button_element(self) -> webdriver:
        return self.driver.find_element_by_xpath(self.parser.parser_unit.button)

    def insert_to_db(self,name,url,pic_url,price,category):
        insert.make_insert_query(name, self.store, url, pic_url, price)

    @staticmethod
    def get_parser(store:str) -> ParserInterface:
        return ParserImpl(store)

    def mining(self, keyword):
        driver = self.driver
        driver.get(self.url)
        self.search_init(keyword)
        front_item_name = ""
        while True:
            data_list = self.parser.parse_to_list(self.driver)
            if len(data_list) == 0 or front_item_name == data_list[0].name:
                break
            else:
                front_item_name = data_list[0].name
            for data in data_list:
                print("""
                name   : %s
                store  : %s
                url    : %s
                pic_url: %s
                price  : %s
                """ % (data.name, self.store, data.url, data.pic_url, data.price))
                #insert().insert_to_db(data.name,data.url,data.pic_url,data.price,data.category)
            if not self.do_next_page():
                break


miner = MinerImpl(None, "G마켓", "http://www.gmarket.co.kr", None)
miner.mining("신발")
