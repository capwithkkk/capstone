from crawler import MinerImpl, ParserImpl


miner = MinerImpl(None, None, None, 0, None, 50)

# name = "G마켓"
# url = "http://www.gmarket.co.kr/"
# flag = 0

name = "11번가"
url = "http://www.11st.co.kr/"
flag = 0

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

# name = "티몬"
# url = "http://www.ticketmonster.co.kr/"
# flag = 4


parser = ParserImpl(name, flag)
miner.set_store(name, url, flag, parser)
miner.mining("티셔츠")