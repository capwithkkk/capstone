import abc,random,heapq,time
from insert import Database
from crawler import MinerImpl
from crawler import ParserImpl
from crawler import ParserUnit
from crawler import DriverHelper
from repeater import Repeater
from selenium.common.exceptions import StaleElementReferenceException
from log import ExceptionWriter, LogWriter, BaseWriter
from Lib.queue import Queue

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


class StoreInfo:

    def __init__(self, store, url, flag):
        self.store = store
        self.url = url
        self.flag = flag
        self.parser = ParserImpl(store, flag)


class Keyword:

    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


class AbstractCollector(abc.ABC):

    @abc.abstractclassmethod
    def init_keyword(self):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def choose_keyword(self) -> Keyword:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def nice(self, keyword:Keyword):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get_all_store_info(self) -> []:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def refresh_keyword(self,keyword:Keyword):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def update_keyword_list(self):
        raise NotImplementedError()

    def run(self):
        self.init_keyword()
        store_info_list = self.get_all_store_info()
        miner = MinerImpl(None, None, None, 0, None, 50)
        while True:
            try:
                keyword = self.choose_keyword()
                for store_info in store_info_list:
                    miner.set_store(store_info.store, store_info.url, store_info.flag, store_info.parser)
                    state_str = "store : " + store_info.store + ", and keyword : " + keyword.name + " and last priority : " + str(keyword.priority)
                    LogWriter.instance().append("MINING LOG : " + state_str)
                    miner.mining(keyword.name)
                self.nice(keyword)
                self.refresh_keyword(keyword)
                self.update_keyword_list()
            except RuntimeError as e:
                ExceptionWriter.instance().append_exception(e)
                pass


class BaseCollector(AbstractCollector):

    def __init__(self,flag):
        self.priority_queue = []
        self.update_required = []
        self.flag = flag

    def init_keyword(self):
        keywords = Database.instance().take_query("SELECT * FROM keyword")
        for keyword in keywords:
            heapq.heappush(self.priority_queue, Keyword(keyword[0],keyword[1]))

    def choose_keyword(self) -> Keyword:
        item = heapq.heappop(self.priority_queue)
        return item

    def nice(self, keyword:Keyword):
        random.seed(a=None)
        keyword.priority += random.randint(320, 450)

    def get_all_store_info(self) -> []:
        store_list = []
        stores = Database.instance().take_query("SELECT store,url,flag FROM store_info WHERE flag = " + str(self.flag) + "")
        for store in stores:
            store_list.append(StoreInfo(store[0],store[1],store[2]))
        return store_list

    def refresh_keyword(self,keyword:Keyword):
        self.update_required.append(keyword)
        heapq.heappush(self.priority_queue, keyword)

    def update_keyword_list(self):
        for keyword in self.update_required:
            Database.instance().take_exe("UPDATE keyword SET priority = " + str(keyword.priority) + " WHERE name = '" + str(keyword.name) + "'")
        self.update_required = []
        for key in self.priority_queue:
            key.priority = int(key.priority * 0.9)


class CategoryCollector:

    def __init__(self, store: str, category_link: str, sub_categories: str, section: str, articles: str, url: str, url_attr: str, categories: str):
        self.store = store
        self.sub_categories = sub_categories
        self.category_link = category_link
        self.section = section
        self.articles = articles
        self.url = url
        self.url_attr = url_attr
        self.categories = categories
        self.button = '.'
        self.is_button_activator = False

    def set_button(self, button):
        self.button = button
        self.is_button_activator = True

    def collect_category(self, init_page: str, init_category: str, init_layer: int, real_category: str):
        print("START COLEECT")
        queue = Queue()
        queue.put([init_page,init_category, init_layer])
        driver = DriverHelper.instance().get_driver()
        while queue.empty() is False:
            elem = queue.get()
            page = elem[0]
            category = elem[1]
            layer= elem[2]
            CategoryCollector.add_category_convergence(category,real_category)
            print("페이지 조회 : " + page)
            if 'javascript:' in page:
                driver.execute_script(page)
            else:
                driver.get(page)
            section = Repeater.repeat_function(driver.find_element_by_xpath,(self.section,),StaleElementReferenceException,6)
            articles = Repeater.repeat_function(section.find_elements_by_xpath,(self.articles,),StaleElementReferenceException,6)
            url0 = Repeater.repeat_function(articles[0].find_element_by_xpath,(self.url,),StaleElementReferenceException,6)
            url = ParserImpl.determine_attr_val(url0, self.url_attr)
            driver.get(url)
            categories = Repeater.repeat_function(driver.find_elements_by_xpath,(self.categories,),StaleElementReferenceException,6)
            if len(categories) > layer+1:
                button = Repeater.repeat_function(categories[layer+1].find_element_by_xpath,(self.button,),StaleElementReferenceException,6)
                if self.is_button_activator is True:
                    driver.execute_script("arguments[0].click()", button)
                    BaseWriter.instance("./temp").append(driver.page_source)
                sub_categories = Repeater.repeat_function(categories[layer+1].find_elements_by_xpath,(self.sub_categories,),StaleElementReferenceException,6)
                for sub_category in sub_categories:
                    page_elem = Repeater.repeat_function(sub_category.find_element_by_xpath,(self.category_link,),StaleElementReferenceException,6)
                    page = page_elem.get_attribute("href")
                    category = page_elem.get_attribute("innerHTML").strip("[]{} \r\n")
                    queue.put([page,category,layer+1])
                    print("큐 삽입 : " + category + ", layer : " + str(layer+1))

    @staticmethod
    def add_category_convergence(name, real_category):
        print("수집 : " + name + "->" + real_category)
        Database.instance().make_query("INSERT INTO `category_convergence` (`origin_name`, `category`) VALUES ('" + name + "', '" + real_category + "');")


