import abc,random,heapq
from insert import Database
from crawler import MinerImpl
from crawler import ParserImpl
from log import ExceptionWriter, LogWriter


class StoreInfo:

    def __init__(self, store, url):
        self.store = store
        self.url = url
        self.parser = ParserImpl(store)


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
        miner = MinerImpl(None, None, None, None, 50)
        while True:
            try:
                keyword = self.choose_keyword()
                for store_info in store_info_list:
                    miner.set_store(store_info.store, store_info.url, store_info.parser)
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
        stores = Database.instance().take_query("SELECT store,url FROM store_info WHERE flag = " + str(self.flag) + "")
        for store in stores:
            store_list.append(StoreInfo(store[0],store[1]))
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


bc = BaseCollector(0)
bc.run()