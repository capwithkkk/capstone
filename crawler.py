import abc, time
from insert import insert
from selenium import webdriver


#todo
class ParserUnit:
    pass


class Data:

    def __init__(self,name,url,pic_url,price,category):
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
    def parse_to_list(self,driver:webdriver) -> Data:
        raise NotImplementedError()


#todo implement
class AbstractParser(ParserInterface):

    def parse_to_list(self,page:str) -> Data:
        list = []
        #todo

        return list
    pass


class MinerInterface(abc.ABC):

    @abc.abstractclassmethod
    def search_init(self,keyword:str):
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
    def insert_to_db(self,name,url,pic_url,price,category):
        raise NotImplementedError()


class MinerImpl(MinerInterface):

    def __init__(self,driver,store,url,parser):
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
        try:
            page_element = self.get_next_button_element()
            if page_element is None:
                return False
            self.driver.execute_script("arguments[0].click()",page_element)
            time.sleep(1)
            return True
        except:
            return False

    #todo
    def get_query_input_element(self) -> webdriver:
        return None

    #todo
    def get_next_button_element(self) -> webdriver:
        return None

    def insert_to_db(self,name,url,pic_url,price,category):
        insert.make_insert_query(name,self.store,url,pic_url,price)

    @staticmethod
    def get_parser(self,store:str) -> ParserInterface:
        return self.parser

    def mining(self,keyword):
        while True:
            driver = self.driver
            driver.get(self.url)
            self.search_init(keyword)
            data_list = self.parser.parse_to_list(self.driver)
            for data in data_list:
                self.insert_to_db(data.name,data.url,data.pic_url,data.price,data.category)
            if not self.do_next_page():
                break


