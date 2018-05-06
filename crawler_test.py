from crawler import MinerImpl, ParserImpl
from concurrent.futures.thread import ThreadPoolExecutor



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


with ThreadPoolExecutor(max_workers=10) as executor:
    try:
        name = "G마켓"
        url = "http://www.gmarket.co.kr/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "11번가"
        url = "http://www.11st.co.kr/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "옥션"
        url = "http://www.auction.co.kr/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "인터파크"
        url = "http://shopping.interpark.com/shopSearch.do?q=$keyword"
        flag = 5
        executor.submit(test, name, url, flag)
        name = "위메프"
        url = "http://www.wemakeprice.com/"
        flag = 4
        executor.submit(test, name, url, flag)
        name = "쿠팡"
        url = "http://www.coupang.com/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "티몬"
        url = "http://www.ticketmonster.co.kr/"
        flag = 4
        executor.submit(test, name, url, flag)

        name = "G마켓"
        url = "http://www.gmarket.co.kr/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "11번가"
        url = "http://www.11st.co.kr/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "옥션"
        url = "http://www.auction.co.kr/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "인터파크"
        url = "http://shopping.interpark.com/shopSearch.do?q=$keyword"
        flag = 5
        executor.submit(test, name, url, flag)
        name = "위메프"
        url = "http://www.wemakeprice.com/"
        flag = 4
        executor.submit(test, name, url, flag)
        name = "쿠팡"
        url = "http://www.coupang.com/"
        flag = 0
        executor.submit(test, name, url, flag)
        name = "티몬"
        url = "http://www.ticketmonster.co.kr/"
        flag = 4
        executor.submit(test, name, url, flag)
    except RuntimeError as e:
        pass