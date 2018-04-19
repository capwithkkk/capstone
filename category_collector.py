from collector import CategoryCollector
from crawler import ParserUnit




# store = "G마켓"
# sub_categories = 'div[@class="loc-catewrap uxerollover"]/*[@class="layer_loc-cate"]/a'
# category_link  = '.'
#
# parser = ParserUnit(store)
# section = parser.section
# articles = parser.articles
# url = parser.url
# url_attr = parser.url_attr
# categories = parser.categories
# home_layer = 0
#
# init_page = "http://category.gmarket.co.kr/listview/List.aspx?gdmc_cd=200000959"
# init_category = "커피/음료"
# init_layer = 1
# real_category = "음료/주류/커피/분유"



# store = "11번가"
# sub_categories = 'div//ul/li'
# category_link  = 'a'
# button = 'button'
# is_activator = True
#
# parser = ParserUnit(store)
# section = parser.section
# articles = parser.articles
# url = parser.url
# url_attr = parser.url_attr
# categories = parser.categories
# home_layer = -1
#
# init_page = "http://www.11st.co.kr/browsing/DisplayCategory.tmall?method=getDisplayCategory2Depth&dispCtgrNo=1001489&dispCtgrCd=v0p001"
# init_category = "커피/생수/음료"
# init_layer = 1
# real_category = "음료/주류/커피/분유"


store = "옥션"
sub_categories = '*[@class="categorylayer"]/*[@class="categorylayerin"]/child::ul/li'
category_link  = 'a'

parser = ParserUnit(store)
section = '//*[@class="list_wrap list_line"]|//*[@id="ucItemList_listview"]'
articles = parser.articles
url = parser.url
url_attr = parser.url_attr
categories = '//*[@class="loc"]/*[@class="category_wrap"]'
home_layer = -1

init_page = "http://listings.auction.co.kr/category/list.aspx?category=51380000"
init_category = "혼합곡/잡곡류"
init_layer = 2
real_category = "쌀/잡곡"


cc = CategoryCollector(
    store,
    category_link,
    sub_categories,
    section,
    articles,
    url,
    url_attr,
    categories)
cc.set_limit(3)
# cc.set_button(button)


cc.collect_category(init_page, init_category, init_layer+home_layer, real_category, is_replace_mode=False)
del cc
