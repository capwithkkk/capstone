CREATE TABLE category(
    	category_id	integer	primary key	AUTO_INCREMENT,
	category_name	varchar(32) unique,
	parent_name	varchar(32),
	foreign key(parent_name) references category(category_name)
);

CREATE TABLE product(
    	pro_index	integer	AUTO_INCREMENT,
	name	varchar(128)	not null,
	store	varchar(32),
	url		varchar(256)	not null,
	pic_url	varchar(256),
	price	int				not null,
	expired	Date,
	category_id	integer,
	foreign key(category_id) references category(category_id),
	primary key(pro_index)
);
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
	primary key(store)
);
CREATE TABLE store_info(
	store    varchar(128)    not null,
	url   	 varchar(256),
	flag	integer,
	primary key(store)
);

CREATE TABLE keyword(
	name    varchar(128)    not null,
	priority   	 integer,
	primary key(name)
);

CREATE TABLE parse_rule_extra(
	store    varchar(128)    not null,
	categories	varchar(128),
	category_core	varchar(128),
	brand   	 varchar(128),
	is_inlink	integer,
	primary key(store)
);
CREATE TABLE category_convergence(
	origin_name    varchar(128)    not null,
	category	varchar(128),
	primary key(origin_name)
);







INSERT INTO category VALUES(1,"��ü","��ü");
INSERT INTO category VALUES(null,"��ǰ","��ü");
INSERT INTO category VALUES(null,"�Ƿ�","��ü");


INSERT INTO product VALUES(null,"������ ���尡�� 1kg","�Ե�Ȩ����","http://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=1013823820","http://image2.lotteimall.com/goods/20/38/82/1013823820_L.jpg",36500,null,2);
INSERT INTO product VALUES(null,"[Ǫ����]��������(4kg)","�̸�Ʈ��","http://emart.ssg.com/item/itemView.ssg?itemId=1000021949490&siteNo=6001&salestrNo=6005","http://item.ssgcdn.com/90/94/94/item/1000021949490_i1_253.jpg",12380,null,2);
INSERT INTO product VALUES(null,"[�����]17FW ���� �����ö�׵� ������� (1BA045_2EVU_F0002_V_OOO_17F)","�����","http://www.hyundaihmall.com/front/pda/itemPtc.do?slitmCd=2058932202","http://image.hyundaihmall.com/static/2/2/93/58/2058932202_0_300.jpg",1960120,null,3);

INSERT INTO parse_rule VALUES(
"G����",
'//*[@id="keyword"]',
'//*[@id="searchListItems"]',
'li',
'*[@class="item_info"]/a/*[@class="title"]',
'*[@class="item_info"]/a',
'*[@class="item_info"]/a/*[@class="thumb"]/img',
'*[@class="price_info"]/*[@class="price"]/a/strong',
'//*[@class="paginate"]/*[@class="button_next"]/a'

);


INSERT INTO parse_rule VALUES(
"����",
'//*[@id="txtKeyword"]',
'//*[@id="ucItemList_listview"]',
'*[@class="list_view "]',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="item_title_wrap"]/*[@class="item_title"]/a',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="item_title_wrap"]/*[@class="item_title"]/a',
'*[@class="layout_left"]/*[@class="image_info"]/*[@class="image"]/a/img',
'*[@class="layout_right"]/*[@class="item_price_info"]/*[@class="item_price"]/strong',
'//*[@class="paginate"]/span/a[@class="on"]/following-sibling::a[1]'

);


INSERT INTO parse_rule VALUES(
'11����',
'//*[@id="AKCKwd"]',
'//*[@id="product_listing"]/div/*[@class="total_listing_wrap"]/*[@class="tt_listbox"]',
'li',
'*[@class="total_listitem"]/*[@class="list_info"]/*[@class="info_tit"]/a',
'*[@class="total_listitem"]/*[@class="list_info"]/*[@class="info_tit"]/a',
'*[@class="total_listitem"]/*[@class="photo_wrap"]/a/img',
'*[@class="total_listitem"]/*[@class="list_price"]/*[@class="price_box"]/*[@class="price_detail"]/strong',
'//*[@id="list_paging"]/span/strong/following::a[contains(@onclick,"goPageNum")][1]'

);


INSERT INTO store_info VALUES("G����","http://www.gmarket.co.kr/",0);
INSERT INTO store_info VALUES("11����","http://www.11st.co.kr/",0);
INSERT INTO store_info VALUES("����","http://www.auction.co.kr/",0);


INSERT INTO keyword VALUES("Ű����1",10);
INSERT INTO keyword VALUES("Ű����2",10);
INSERT INTO keyword VALUES("Ű����3",10);
INSERT INTO keyword VALUES("Ű����4",10);
INSERT INTO keyword VALUES("Ű����5",10);


INSERT INTO parse_rule_extra VALUES(
'G����',
'//*[@class="location-navi"]/ul/li',
'a',
'//*[@id="vip-tab_detail"]/*[@class="vip-detailarea_productinfo"]/*[@class="table_productinfo"][1]/tbody/tr[th = "�귣��"]/td',
1
);

INSERT INTO parse_rule_extra VALUES(
'11����',
'//*[@id="wrapBody"]/*[@class="location_wrap"]/div',
'button',
'//*[@id="tabProductInfo"]/*[@class="prdc_detail_table"]/tbody/tr[th = "�귣��"]/td',
1
);

INSERT INTO parse_rule_extra VALUES(
'����',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="category"]/a',
'.',
'*[@class="layout_left"]/*[@class="item_title_info"]/*[@class="item_title_wrap"]/*[@class="promotion"]/*[@class="pmtxt"]',
0
);
