import abc
import time
from repeater import Repeater
from insert import Database
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, UnexpectedAlertPresentException, WebDriverException
from singleton import SingletonInstance
from pymysql.err import Error
import lxml.html as lhtml
from lxml.html import HtmlElement
from log import SubstitutionTrialWriter, ExceptionWriter


# 클레스
# 크롤링을 위해 사이트 마다 정해진 xpath 정보가 담긴 튜플, 생성시 데이터베이스로 부터 초기화된 값이 로드된다.
# 필드변수 :
# store: str, rules: ParserImpl, search: str, section: str,
# articles: str, name: str, url: str, pic_url: str, price: str
# button: str, name_attr: str, url_attr: str, pic_url_attr: str, price_attr: str
# categories: str, category_core: str, brand: str, in_link: str
class ParserUnit:

    def __init__(self, store: str):
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

    # 함수
    # 검색창,색션,아티클, 아티클내 이름,url,가격등과 pagination 버튼의 parse_rule 데이터베이스 컬럼을 구한다.
    # 입력 : None
    # 출력 : str[][]
    def get_parse_rule(self) -> []:
        return Database.instance().take_query(
            "SELECT search,section,articles,name,url,pic_url,price,button,name_attr,url_attr,pic_url_attr,price_attr "
            "FROM parse_rule WHERE store = '" + self.store + "'"
        )

    # 함수
    # 카테고리, 브랜드 항목 관련 parse_rule 데이터베이스 컬럼을 구한다.
    # 입력 : None
    # 출력 : str[][]
    def get_parse_rule_extra(self):
        return Database.instance().take_query(
            "SELECT categories,category_core,brand,is_inlink FROM parse_rule_extra WHERE store = '" + self.store + "'"
        )


# 데이터
# 사실상 상품 정보 튜플을 클레스를 이용하여 구현, 구조체와 유사.
# 필드변수 : name: str, url: str, pic_url: str, price: str, category: str, brand: str
class Data:

    def __init__(self, name: str, url: str, pic_url: str, price: str, category: str, brand: str):
        self.name = name
        self.url = url
        self.pic_url = pic_url
        self.price = price
        self.category = category
        self.brand = brand


# 클레스
# 카테고리 이름을 키로, 고유 인덱스 번호를 값을 가지는 Dictionary 를 싱글턴 객체로 외부에서 쓸 수 있도록 모듈화 함.
# 필드변수 : categories: dictionary{key: str, value: str}, unclassified_categories: str[]
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

    # 함수
    # 카테고리 id, 이름쌍의 데이터베이스 컬럼을 구한다.
    # 입력 : None
    # 출력 : str[][]
    @staticmethod
    def get_categories():
        return Database.instance().take_query("SELECT category_id, category_name FROM category")

    # 함수
    # 미분류 카테고리 이름 데이터베이스 컬럼을 구한다.
    # 입력 : None
    # 출력 : str[][]
    @staticmethod
    def get_unclassified_categories():
        return Database.instance().take_query("SELECT category_name FROM category WHERE parent_name = '미분류'")


# 클레스
# 카테고리 치환식에 따라 크롤러가 임의로 획득한 카테고리 이름을 가지고 실제 데이터베이스 category 영역에 속하는 카테고리 이름으로 일괄 치환할 수 있도록 만듬.
# 내부 함수 작동을 위해 한번 초기화 된 후 사용된다.
# 필드변수 : dict: dictionary{key: str, value: str}
class CategoryConverger(SingletonInstance):

    def __init__(self):
        self.rules = CategoryConverger.get_category_converger()
        self.dict = {}
        for rule in self.rules:
            self.dict[rule[0]] = rule[1]

    # 함수
    # 실제 카테고리 치환식에 따라 name 을 카테고리 이름으로 치환한다.
    # 입력 : name: str
    # 출력 : str
    def substitute_category(self, name: str):
        if name in self.dict:
            return self.dict[name]
        else:
            return None

    # 함수
    # 카테고리 치환식 데이터베이스 컬럼을 구한다.
    # 입력 : None
    # 출력 : str[][]
    @staticmethod
    def get_category_converger():
        return Database.instance().take_query("SELECT * from category_convergence")


# 인터페이스
# 이 인터페이스를 구현한 클레스는 웹 드라이버로 부터 상품 Data 리스트를 추출 할 수 있다.
class ParserInterface(abc.ABC):

    # 함수
    # 웹 드라이버로 부터 Data 리스트를 얻는다.
    # 입력 : driver: webdriver
    # 출력 : Data[]
    @abc.abstractclassmethod
    def parse_to_list(self, driver: webdriver) -> []:
        raise NotImplementedError()


# 클레스
# ParserInterface 를 구현한 클레스, selenium webdriver를 이용하였다.
# 필드변수 : store: str, parser_unit: ParserImpl
class ParserImpl(ParserInterface):

    def __init__(self, store: str):
        self.store = store
        self.parser_unit = ParserUnit(store)

    # 함수
    # selenium http DOM 객체(주로 html 태그)와 attribute 이름 정보를 받아. 만약 attr 이 비어있다면 DOM 객체의 innerHTML 의 값을,
    # 그렇지 않으면 attr 의 이름에 해당하는 value 를 얻는다.
    # 입력 : driver: selenium webdriver htmlElement, attr: str
    # 출력 : str
    @staticmethod
    def determine_attr_val(driver: webdriver, attr: str):
        if attr is None:
            return driver.text
        else:
            return driver.get_attribute(attr)

    # 함수
    # ParserInterface로 부터 Implement
    def parse_to_list(self, driver: webdriver) -> []:
        rule_list = []
        try:

            section = driver.find_element_by_xpath(self.parser_unit.section)
            articles = section.find_elements_by_xpath(self.parser_unit.articles)

            for article in articles:
                name0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.name},StaleElementReferenceException,2)
                name = ParserImpl.determine_attr_val(name0, self.parser_unit.name_attr)
                name = name.strip("\"\'\r\n")
                url0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.url},StaleElementReferenceException,2)
                url = ParserImpl.determine_attr_val(url0, self.parser_unit.url_attr)
                pic_url0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.pic_url},StaleElementReferenceException,2)
                pic_url = ParserImpl.determine_attr_val(pic_url0, self.parser_unit.pic_url_attr)
                price0 = Repeater.repeat_function(article.find_element_by_xpath,{self.parser_unit.price},StaleElementReferenceException,2)
                price = ParserImpl.determine_attr_val(price0, self.parser_unit.price_attr)
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

    # 함수
    # selenium http DOM 객체(주로 html 태그)에서 parse_rule(xpath 형태) 를 이용하여 특정 부분의 텍스트를 추출한다.
    # 입력 : driver: selenium webdriver htmlElement, parse_rule: str
    # 출력 : str
    @staticmethod
    def find_item_info(driver: webdriver, parse_rule: str) -> str:
        try:
            elem = ParserImpl.out_from_xpath(driver, parse_rule)
            text = elem[0].text
            text = text.strip("()[]{} \r\n")
            return text
        except IndexError:
            return "N/A"

    # 함수
    # selenium http DOM 객체(주로 html 태그)에서 categories(xpath 형태)를 이용하여 상품의 카테고리 영역을 전부 포함하는 DOM 객체를 찾은뒤,
    # 여기에서 category_unit(xpath 형태)를 통해 category 의 상분류, 중분류, 하분류, ..
    # 기타 세부분류에 해당되는 카테고리 영역의 텍스트 리스트를 추출한뒤,
    # 텍스트 리스트내 카테고리 치환식을 거쳐, 현재 사용중인 카테고리 이름을 추출하거나,
    # 없는 경우 미분류 카테고리 항목으로 새로 데이터베이스 컬럼을 만든뒤, 임의로 배정한다음, 다시 해당하는 카테고리 이름을 리턴한다.
    # 입력 : driver: selenium webdriver htmlElement, categories: str, category_unit: str
    # 출력 : str
    # 예외 : NoSuchElementException
    @staticmethod
    def find_category_info(driver: webdriver, categories: str, category_unit: str) -> str:
        try:
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
                    SubstitutionTrialWriter.instance().append(category)
            if empty_sub_category_name not in CategoryDict.instance().unclassified_categories:
                CategoryDict.instance().unclassified_categories.append(empty_sub_category_name)
                Database.instance().make_query(
                    'INSERT INTO category VALUES(null,"' + empty_sub_category_name + '", "미분류")'
                )
                category_index = Database.instance().take_query(
                    'SELECT category_id FROM category WHERE category_name = "' + empty_sub_category_name + '"'
                )[0][0]
                CategoryDict.instance().categories[empty_sub_category_name] = category_index
            return empty_sub_category_name
        except (NoSuchElementException, IndexError):
            raise NoSuchElementException

    # 함수
    # HtmlElement 이나, 어떤 형식인지 모르는 임의의 root 와 xpath 식을 받아,
    # lxmlElement 일때와 seleniumElement 일때 두가지 경우 자동으로 xpath 를 거친 필터링된 htmlElement 을 내놓으며,
    # 이외에 경우 None 을 리턴한다.
    # 입력 : driver: selenium webdriver htmlElement, categories: str, category_unit: str
    # 출력 : htmlElement
    # 예외 : NoSuchElementException
    @staticmethod
    def out_from_xpath(root, xpath: str) -> object:
        try:
            if isinstance(root, WebElement) or isinstance(root, WebDriver):
                return root.find_elements_by_xpath(xpath)
            elif isinstance(root, HtmlElement):
                return root.xpath(xpath)
            return None
        except (UnexpectedAlertPresentException,NoSuchElementException):
            raise NoSuchElementException


# 인터페이스
# 크롤링에서 가장 필수적이며 기초적인 메소드, search / pagination / extraction / data_insertion 4개의 메소드의 원형의 표준을 정의해 놓았다.
class MinerInterface(abc.ABC):

    # 프로시저
    # 키워드를 통해 검색을 시도한다.
    # 입력 : driver: keyword:str
    @abc.abstractclassmethod
    def search_init(self, keyword:str):
        raise NotImplementedError()

    # 함수
    # 다음 페이지로 이동 한다. 만약 마지막 페이지 일시 False 를, 그 이외에는 True 를 리턴한다.
    # 입력 : None
    # 출력 : bool
    @abc.abstractclassmethod
    def do_next_page(self) -> bool:
        raise NotImplementedError()

    # 함수
    # 현재 store 이름을 내놓는다.
    # 입력 : None
    # 출력 : store: str
    @abc.abstractclassmethod
    def get_store(self) -> str:
        raise NotImplementedError()

    # 함수
    # 현재 HtmlEntity 를 내놓는다. HtmlEntity 는 Html root 에 해당하는 htmlElement 이다.
    # 입력 : None
    # 출력 : HtmlEntity
    @abc.abstractclassmethod
    def get_entity(self) -> object:
        raise NotImplementedError()

    # 함수
    # 사이트 메인에서, keyword 를 입력할 input에 해당하는 htmlElement 를 내놓는다.
    # 입력 : None
    # 출력 : HtmlElement
    @abc.abstractclassmethod
    def get_query_input_element(self) -> object:
        raise NotImplementedError()

    # 함수
    # 검색 이후 다음 페이지 button 에 해당하는 htmlElement 를 내놓는다.
    # 입력 : None
    # 출력 : HtmlElement
    @abc.abstractclassmethod
    def get_next_button_element(self) -> object:
        raise NotImplementedError()

    # 프로시저
    # 실제 Data 에 해당하는 정보를 database 에 넣는다.
    # 입력 : data: Data
    @abc.abstractclassmethod
    def insert_to_db(self, data: Data):
        raise NotImplementedError()


# 클레스
# DriverHelper 라는 보조 웹 드라이버를 위한 싱글턴 클레스.
class DriverHelper(SingletonInstance):

    def __init__(self):
        self.driver = MinerImpl.create_driver()

    def get_driver(self):
        return self.driver


# 클레스
# MinerInterface 를 구현한 클레스이다. selenium webdriver를 이용하였다. limit 값은 사이트당 수집량의 사용자 정의 한계값이다.
# 필드 : driver: webdriver, store: str, url: str, parser: ParserInterface, limit: int
class MinerImpl(MinerInterface):

    def __init__(self, driver: webdriver, store: str, url: str, parser: ParserInterface, limit: int):
        self.store = store
        self.url = url
        self.limit = limit
        if parser is None and store is not None:
            self.parser = MinerImpl.get_parser(self.store)
        else:
            self.parser = parser
        if driver is None:
            self.driver = MinerImpl.create_driver()
        else:
            self.driver = driver

    # 함수
    # 새로운 웹 드라이버를 생성한다
    # 입력 : None
    # 출력 : selenium webdriver
    @staticmethod
    def create_driver() -> webdriver:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument("--disable-extensions")
        prefs = {"profile.managed_default_content_settings.images":2}
        option.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(chrome_options=option, executable_path="./chrome/chromedriver")

    # 함수
    # store 이름을 통해 파셔 객체를 생성한다
    # 입력 : store: str
    # 출력 : ParserInterface
    @staticmethod
    def get_parser(store: str) -> ParserInterface:
        return ParserImpl(store)

    # 함수
    # MinerInterface 부터 Implement
    def get_store(self) -> str:
        return self.store

    # 함수
    # MinerInterface 부터 Implement
    def get_entity(self) -> webdriver:
        return self.driver

    # 프로시저
    # store, url, parser 를 초기화한다.
    # 입력 : store: str, url: str, parser: ParserInterface
    def set_store(self, store: str, url: str, parser: ParserInterface):
        self.store = store
        self.url = url
        self.parser = parser

    # 함수
    # MinerInterface 부터 Implement
    def search_init(self,keyword:str):
        driver_element = self.get_query_input_element()
        driver_element.send_keys(keyword)
        driver_element.submit()

    # 함수
    # MinerInterface 부터 Implement
    def do_next_page(self) -> bool:
        page_element = self.get_next_button_element()
        if page_element is None:
            return False
        self.driver.execute_script("arguments[0].click()", page_element)
        return True

    # 함수
    # MinerInterface 부터 Implement
    def get_query_input_element(self) -> webdriver:
        return self.driver.find_element_by_xpath(self.parser.parser_unit.search)

    # 함수
    # MinerInterface 부터 Implement
    def get_next_button_element(self) -> webdriver:
        try:
            return self.driver.find_element_by_xpath(self.parser.parser_unit.button)
        except NoSuchElementException:
            return None

    # 함수
    # MinerInterface 부터 Implement
    def insert_to_db(self, data: Data):
        Database.instance().make_insert_query(data.name, self.store, data.url, data.pic_url, data.price, CategoryDict.instance().categories[data.category], data.brand)

    # 프로시저
    # 크롤링을 시작한다. pagination 이 끝날 때 까지 혹은 수집 상품 Data량이 limit 값을 초과할때 까지 무한 반복한다.
    # 입력 : keyword: str
    def mining(self, keyword: str):
        try:
            driver = self.driver
            driver.get(self.url)
            self.search_init(keyword)
        except WebDriverException as e:
            print("WebDriverException occurred during init process. "
                  "The site is may carrying out temporary- or regular inspection.")
            ExceptionWriter.instance().append_exception(e)
            return
        front_item_name = ""
        page = 1
        limit_count = 0
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
                            self.insert_to_db(data)
                            limit_count += 1
                        except (KeyError, Error) as e:
                            print("Insertion failed.")
                            ExceptionWriter.instance().append_exception(e)
                if not self.do_next_page():
                    break
                if limit_count > self.limit:
                    break
                page += 1
                page_parsing_flag = False
            except StaleElementReferenceException:
                time.sleep(0.1)
            except WebDriverException as e:
                print("WebDriverException occurred. The crawling has been postponed until next keyword routine")
                ExceptionWriter.instance().append_exception(e)
                break
