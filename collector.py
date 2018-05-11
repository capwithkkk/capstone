import abc,random,heapq,time,copyreg,types
from insert import Database
from crawler import MinerImpl
from crawler import ParserImpl
from crawler import DriverHelper
from repeater import Repeater
from selenium.common.exceptions import StaleElementReferenceException,WebDriverException
from log import ExceptionWriter, LogWriter
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue
import signal
import os
import asyncio
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
    def refresh_keyword(self, keyword:Keyword):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def update_keyword_list(self):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def interrupt(self, signum, frame):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get_future_list(self) -> []:
        raise NotImplementedError()

    def run(self, max_thread: int=1):
        self.init_keyword()
        store_info_list = self.get_all_store_info()
        signal.signal(signal.SIGINT, self.interrupt)
        signal.signal(signal.SIGTERM, self.interrupt)
        loop = asyncio.get_event_loop()
        future_list = self.get_future_list()
        while True:
            try:
                keyword = self.choose_keyword()
                for store_info in store_info_list:
                    while len(future_list) >= max_thread:
                        for future in future_list:
                            if future.done() and (future.result() is None or future.result() is 0):
                                print("Result param : " + str(future.result()))
                                future_list.remove(future)
                        time.sleep(1)
                    print("Coroutine " + str(len(future_list)))
                    f = loop.run_until_complete(self.miner_routine(store_info, keyword))
                    future_list.append(f)
                self.nice(keyword)
                self.refresh_keyword(keyword)
                self.update_keyword_list()
                print("Next Keywords")
            except RuntimeError as e:
                raise e
                #ExceptionWriter.instance().append_exception(e)
                pass

    @staticmethod
    async def miner_routine(store_info, keyword):
        print("Routine Start...")
        miner = MinerImpl(None, None, None, 0, None, 50)
        miner.set_store(store_info.store, store_info.url, store_info.flag, store_info.parser)
        state_str = "store : " + store_info.store + ", and keyword : " + keyword.name + " and last priority : " + str(keyword.priority)
        LogWriter.instance().append("MINING LOG : " + state_str)
        out = await miner.mining(keyword.name)
        print("Mining End...")
        return out
        # miner.close()
        # del miner


class BaseCollector(AbstractCollector):

    def __init__(self):
        self.priority_queue = []
        self.update_required = []
        self.futures = []

    def __del__(self):
        del self.priority_queue
        del self.update_required
        for future in self.futures:
            future.cancel()

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

    def interrupt(self, signum, frame):
        self.__del__()

    def get_future_list(self) -> []:
        return self.futures

    def get_all_store_info(self) -> []:
        store_list = []
        stores = Database.instance().take_query("SELECT store,url,flag FROM store_info")
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

    max_query_for_category = 3

    def __init__(self, store: str, category_link: str, sub_categories: str, section: str, articles: str, url: str, url_attr: str, categories: str, limit: int=5):
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
        self.limit = limit

    def __del__(self):
        DriverHelper.instance().destroy()

    def set_button(self, button):
        self.button = button
        self.is_button_activator = True

    def set_limit(self, limit):
        self.limit = limit

    def collect_category(self, init_page: str, init_category: str, init_layer: int, real_category: str, is_replace_mode: bool):
        print("START COLEECT")
        queue = Queue()
        queue.put([init_page,init_category, init_layer])
        driver = DriverHelper.instance().get_driver()
        CategoryCollector.add_category_convergence(init_category,real_category, is_replace_mode)
        while queue.empty() is False:
            try:
                elem = queue.get()
                page = elem[0]
                layer= elem[2]
                print("페이지 조회 : " + page)
                if 'javascript:' in page:
                    driver.execute_script(page)
                else:
                    driver.get(page)
                section = Repeater.repeat_function(driver.find_element_by_xpath,(self.section,), StaleElementReferenceException,6)
                articles = Repeater.repeat_function(section.find_elements_by_xpath,(self.articles,), StaleElementReferenceException,6)
            except WebDriverException:
                continue
            unit = 0
            while True:
                try:
                    url0 = Repeater.repeat_function(articles[unit].find_element_by_xpath,(self.url,), StaleElementReferenceException,6)
                    url = ParserImpl.determine_attr_val(url0, self.url_attr)
                    driver.get(url)
                    categories = Repeater.repeat_function(driver.find_elements_by_xpath,(self.categories,),StaleElementReferenceException,6)
                    if len(categories) > layer+1:
                        button = Repeater.repeat_function(categories[layer+1].find_element_by_xpath,(self.button,),StaleElementReferenceException,6)
                        if self.is_button_activator is True:
                            driver.execute_script("arguments[0].click()", button)
                        sub_categories = Repeater.repeat_function(categories[layer+1].find_elements_by_xpath,(self.sub_categories,),StaleElementReferenceException,6)
                        for sub_category in sub_categories:
                            page_elem = Repeater.repeat_function(sub_category.find_element_by_xpath,(self.category_link,),StaleElementReferenceException,6)
                            page = page_elem.get_attribute("href")
                            category = page_elem.get_attribute("innerHTML").strip("[]{}\r\n 		").replace("<em>", "").replace("</em>", "")
                            CategoryCollector.add_category_convergence(category, real_category, is_replace_mode)
                            category_list = category.split("/")
                            for subcategory in category_list:
                                CategoryCollector.add_category_convergence(subcategory, real_category, is_replace_mode)
                            if layer < self.limit-1:
                                queue.put([page,category,layer+1])
                                print("큐 삽입 : " + category + ", layer : " + str(layer+1))
                    break
                except WebDriverException as e:
                    if unit > CategoryCollector.max_query_for_category:
                        break
                    else:
                        unit += 1

    @staticmethod
    def add_category_convergence(name, real_category, is_replace: bool):
        print("수집 : " + name + "->" + real_category)
        if is_replace:
            Database.instance().make_query("REPLACE INTO `category_convergence` (`origin_name`, `category`) VALUES ('" + name + "', '" + real_category + "');")
        else:
            Database.instance().make_query("INSERT INTO `category_convergence` (`origin_name`, `category`) VALUES ('" + name + "', '" + real_category + "');")

    @staticmethod
    def spliter_insert():
        categories = Database.instance().take_query("SELECT * FROM `category_convergence` WHERE origin_name LIKE '%/%'")
        for category in categories:
            category_list = category[0].split("/")
            for subcategory in category_list:
                Database.instance().make_query("INSERT INTO `category_convergence` (`origin_name`, `category`) VALUES ('" + subcategory + "', '" + category[1] + "');")

