CREATE TABLE category(
    	category_id	integer	primary key	AUTO_INCREMENT,
	category_name	varchar(128) unique,
	parent_name	varchar(128),
	foreign key(parent_name) references category(category_name)
) CHARSET=utf8 COLLATE utf8_bin;

CREATE TABLE product(
    	pro_index	integer	AUTO_INCREMENT,
	name	varchar(128)	not null,
	store	varchar(32),
	url		varchar(256)	not null,
	pic_url	varchar(256),
	price	int				not null,
	expired	Date,
	category_id	integer,
	brand	varchar(256),
	foreign key(category_id) references category(category_id),
	primary key(pro_index),
	unique(name,store,price),
	FULLTEXT (name, brand)
) ENGINE=InnoDB CHARSET=utf8 COLLATE utf8_bin;

CREATE TABLE parse_rule(
	store    varchar(128)    not null,
	search	varchar(128),
	section   	 varchar(128),
	articles    varchar(256),
	name    varchar(256),
	url   	 varchar(256),
	pic_url    varchar(256),
	price    varchar(256),
	button	 varchar(128),
	name_attr	 varchar(128),
	url_attr	 varchar(128),
	pic_url_attr	 varchar(128),
	price_attr	 varchar(128),
	primary key(store)
) CHARSET=utf8 COLLATE utf8_bin;

CREATE TABLE store_info(
	store    varchar(128)    not null,
	url   	 varchar(256),
	flag	integer,
	primary key(store)
) CHARSET=utf8 COLLATE utf8_bin;

CREATE TABLE keyword(
	name    varchar(128)    not null,
	priority   	 integer,
	primary key(name)
) CHARSET=utf8 COLLATE utf8_bin;

CREATE TABLE parse_rule_extra(
	store    varchar(128)    not null,
	categories	varchar(128),
	category_core	varchar(128),
	brand   	 varchar(128),
	is_inlink	integer,
	primary key(store)
) CHARSET=utf8 COLLATE utf8_bin;

CREATE TABLE category_convergence(
	origin_name    varchar(128)    not null,
	category	varchar(128),
	primary key(origin_name)
) CHARSET=utf8 COLLATE utf8_bin;





REPLACE INTO parse_rule VALUES(
"G����",
'//*[@id="keyword"]',
'//*[@id="searchListItems"]',
'li',
'*[@class="item_info"]/a/*[@class="title"]',
'*[@class="item_info"]/a',
'*[@class="item_info"]/a/*[@class="thumb"]/img',
'*[@class="price_info"]/*[@class="price"]/a/strong',
'//*[@class="paginate"]/*[@class="button_next"]/a',
null,
'href',
'src',
null

);


REPLACE INTO parse_rule VALUES(
"����",
'//*[@id="txtKeyword"]',
'//*[@id="ucItemList_listview"]',
'*[@class="list_view "]',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="item_title_wrap"]/*[@class="item_title"]/a',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="item_title_wrap"]/*[@class="item_title"]/a',
'*[@class="layout_left"]/*[@class="image_info"]/*[@class="image"]/a/img',
'*[@class="layout_right"]/*[@class="item_price_info"]/*[@class="item_price"]/strong',
'//*[@class="paginate"]/span/a[@class="on"]/following-sibling::a[1]',
null,
'href',
'data-original',
null

);


REPLACE INTO parse_rule VALUES(
'11����',
'//*[@id="AKCKwd"]',
'//*[@id="product_listing"]//ul',
'li',
'div//img[@class="lazy"]',
'div//a[@data-log-actionid-label="product"]',
'div//img[@class="lazy"]',
'div//strong[@class="sale_price"]',
'//*[@id="list_paging"]/span/strong/following::a[contains(@onclick,"������")][1]',
'alt',
'href',
'data-original',
null

);


REPLACE INTO parse_rule VALUES(
'������ũ',
null,
'//*[@class="productSortingList listViewType"]',
'div/ul/li[@class="goods  "]',
'*[@class="info"]/*[@class="name"]',
'*[@class="info"]/*[@class="name"]',
'*[@class="imgBox"]/a/img',
'*[@class="priceArea"]/*[@class="price"]/a/*[@class="won"]/strong',
'//*[@class="pagingWrap"]/*[@class="nextBox active"]/a[1]',
null,
'href',
'src',
null

);


REPLACE INTO parse_rule VALUES(
'������',
'//*[@id="searchKeyword"]',
'//*[@id="search_deal_area"]',
'li',
'span/a/*[@class="box_desc"]/*[@class="tit_desc"]',
'span/a',
'span/a/*[@class="box_thumb"]/img',
'span/a/*[@class="box_desc"]/*[@class="txt_info"]/*[@class="price"]/*[@class="sale"]',
null,
null,
'href',
'src',
null

);

REPLACE INTO parse_rule VALUES(
'����',
'//*[@id="headerSearchKeyword"]',
'//*[@id="productList"]',
'li',
'a/*[@class="search-product-wrap"]/*[@class="descriptions"]/*[@class="descriptions-inner"]/*[@class="name"]',
'*[@class="search-product-link"]',
'a/*[@class="search-product-wrap"]/*[@class="image"]/img',
'a/*[@class="search-product-wrap"]/*[@class="descriptions"]/*[@class="descriptions-inner"]/*[@class="price-area"]/*[@class="price-wrap"]//*[@class="price-value"]',
'//*[@class="search-pagination"]/a[@class="btn-next"]',
null,
'href',
'src',
null

);


REPLACE INTO parse_rule VALUES(
'Ƽ��',
'//*[@id="top_srch"]',
'//*[@id="_resultDeals"]',
'li',
'*[@class="deal_item_anchor"]/*[@class="deal_item_body"]/*[@class="deal_item_body_top"]/strong',
'*[@class="deal_item_anchor"]',
'*[@class="deal_item_anchor"]/*[@class="deal_item_thumb"]/img',
'*[@class="deal_item_anchor"]/*[@class="deal_item_body"]/*[@class="deal_item_body_middle"]/*[@class="deal_item_price"]/em',
null,
null,
'href',
'src',
null

);


REPLACE INTO store_info VALUES("G����","http://www.gmarket.co.kr/",0);
REPLACE INTO store_info VALUES("11����","http://www.11st.co.kr/",0);
REPLACE INTO store_info VALUES("����","http://www.auction.co.kr/",0);
REPLACE INTO store_info VALUES("������ũ","http://shopping.interpark.com/shopSearch.do?q=$keyword",5);
REPLACE INTO store_info VALUES("������","http://www.wemakeprice.com/",4);
REPLACE INTO store_info VALUES("����","http://www.coupang.com/",0);
REPLACE INTO store_info VALUES("Ƽ��","http://www.ticketmonster.co.kr/",4);





REPLACE INTO parse_rule_extra VALUES(
'G����',
'//*[@class="location-navi"]/ul/li',
'a',
'//*[@id="vip-tab_detail"]/*[@class="vip-detailarea_productinfo"]/*[@class="table_productinfo"][1]/tbody/tr[th = "�귣��"]/td',
1
);

REPLACE INTO parse_rule_extra VALUES(
'11����',
''//*[@class="location_wrap"]/div'',
'button',
'//*[@id="tabProductInfo"]/*[@class="prdc_detail_table"]/tbody/tr[th = "�귣��"]/td',
1
);

REPLACE INTO parse_rule_extra VALUES(
'����',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="category"]/a',
'.',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="item_title_wrap"]/*[@class="promotion"]/*[@class="pmtxt"]',
0
);

REPLACE INTO parse_rule_extra VALUES(
'������ũ',
'//ul[@class="location"]/li',
'a',
'//*[@id="productInfoProvideNotification"]/*[@class="infoContent noline"]/dl[dt = "�귣��"]/dd',
1
);

REPLACE INTO parse_rule_extra VALUES(
'������',
'//*[@class="page-navigation"]/*[@class="select-list-group"]',
'*[@class="action-select"]',
'null',
1
);

REPLACE INTO parse_rule_extra VALUES(
'����',
'//*[@id="breadcrumb"]/li',
'*[@class="breadcrumb-link"]',
'null',
1
);

REPLACE INTO parse_rule_extra VALUES(
'Ƽ��',
'//*[@class="path_nav"]/div',
'a',
'null',
1
);
