from crawler import MinerImpl, ParserImpl
from concurrent.futures.thread import ThreadPoolExecutor
import time



# name = "G마켓"
# url = "http://www.gmarket.co.kr/"
# flag = 0

# name = "11번가"
# url = "http://www.11st.co.kr/"
# flag = 0

# name = "옥션"
# url = "http://www.auction.co.kr/"
# flag = 0

# name = "인터파크"
# url = "http://shopping.interpark.com/shopSearch.do?q=$keyword"
# flag = 5

# name = "위메프"
# url = "http://www.wemakeprice.com/"
# flag = 4

# name = "쿠팡"
# url = "http://www.coupang.com/"
# flag = 0

name = "티몬"
url = "http://www.ticketmonster.co.kr/"
flag = 4


def test(name, url, flag):
    miner = MinerImpl(None, None, None, 0, None, 10)
    parser = ParserImpl(name, flag)
    miner.set_store(name, url, flag, parser)
    miner.mining("주방용 칼")

max_thread = 7
with ThreadPoolExecutor(max_workers=max_thread) as executor:
    list = []
    try:
        name = "G마켓"
        url = "http://www.gmarket.co.kr/"
        flag = 0
        list.append(executor.submit(test, name, url, flag))
        name = "11번가"
        url = "http://www.11st.co.kr/"
        flag = 0
        list.append(executor.submit(test, name, url, flag))
        name = "옥션"
        url = "http://www.auction.co.kr/"
        flag = 0
        list.append(executor.submit(test, name, url, flag))
        name = "인터파크"
        url = "http://shopping.interpark.com/shopSearch.do?q=$keyword"
        flag = 5
        list.append(executor.submit(test, name, url, flag))
        name = "위메프"
        url = "http://www.wemakeprice.com/"
        flag = 4
        list.append(executor.submit(test, name, url, flag))
        name = "쿠팡"
        url = "http://www.coupang.com/"
        flag = 0
        list.append(executor.submit(test, name, url, flag))
        name = "티몬"
        url = "http://www.ticketmonster.co.kr/"
        flag = 4
        list.append(executor.submit(test, name, url, flag))
        #
        # name = "G마켓"
        # url = "http://www.gmarket.co.kr/"
        # flag = 0
        # list.append(executor.submit(test, name, url, flag))
        # name = "11번가"
        # url = "http://www.11st.co.kr/"
        # flag = 0
        # list.append(executor.submit(test, name, url, flag))
        # name = "옥션"
        # url = "http://www.auction.co.kr/"
        # flag = 0
        # list.append(executor.submit(test, name, url, flag))
        # name = "인터파크"
        # url = "http://shopping.interpark.com/shopSearch.do?q=$keyword"
        # flag = 5
        # list.append(executor.submit(test, name, url, flag))
        # name = "위메프"
        # url = "http://www.wemakeprice.com/"
        # flag = 4
        # list.append(executor.submit(test, name, url, flag))
        # name = "쿠팡"
        # url = "http://www.coupang.com/"
        # flag = 0
        # list.append(executor.submit(test, name, url, flag))
        # name = "티몬"
        # url = "http://www.ticketmonster.co.kr/"
        # flag = 4
        # list.append(executor.submit(test, name, url, flag))
        while len(list) >= max_thread:
            print("대기 for : " + str(len(list)))
            for future in list:
                if future.done():
                    print("END? final value : " + future.result)
                    list.remove(future)
            time.sleep(1)
        # time.sleep(100)
    except RuntimeError as e:
        pass