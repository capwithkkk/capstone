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
	primary key(pro_index),
	unique key(name,store)
);



INSERT INTO category VALUES(1,"��ü","��ü");
INSERT INTO category VALUES(null,"��ǰ","��ü");
INSERT INTO category VALUES(null,"�Ƿ�","��ü");



INSERT INTO product VALUES(null,"������ ���尡�� 1kg","�Ե�Ȩ����","http://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=1013823820","http://image2.lotteimall.com/goods/20/38/82/1013823820_L.jpg",36500,null,2);
INSERT INTO product VALUES(null,"[Ǫ����]��������(4kg)","�̸�Ʈ��","http://emart.ssg.com/item/itemView.ssg?itemId=1000021949490&siteNo=6001&salestrNo=6005","http://item.ssgcdn.com/90/94/94/item/1000021949490_i1_253.jpg",12380,null,2);
INSERT INTO product VALUES(null,"[�����]17FW ���� �����ö�׵� ������� (1BA045_2EVU_F0002_V_OOO_17F)","�����","http://www.hyundaihmall.com/front/pda/itemPtc.do?slitmCd=2058932202","http://image.hyundaihmall.com/static/2/2/93/58/2058932202_0_300.jpg",1960120,null,3);