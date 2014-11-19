#提取wb_cnt_num,wb_person_num,wb_repeat_num,wb_loc_num四个特征,并更新
create table wbinfo_tmp_why as select t.event_id,COUNT(w.url_crc) as wb_cnt_num,count(DISTINCT w.url_crc) as wb_person_num,(COUNT(w.url_crc)-count(DISTINCT w.url_crc)) as wb_repeat_num,count(DISTINCT w.location) as wb_loc_num from t_lable_filtered as t inner JOIN w_user_info_distinct as w on t.siteurl_crc=w.url_crc  GROUP BY event_id order by t.event_id
UPDATE event_attributes ea, wbinfo_tmp_why wtw SET
		ea.wb_cnt_num=wtw.wb_cnt_num,
        ea.wb_person_num=wtw.wb_person_num,
		ea.wb_repeat_num=wtw.wb_repeat_num,
		ea.wb_loc_num=wtw.wb_loc_num
        WHERE ea.event_id = wtw.event_id;
drop table wbinfo_tmp_why

#选择地点信息，并下载成文本文件到本地；运行python程序得出每个事件的信息
select event_id,addr_title,addr_content from event_attributes ORDER BY event_id
#把event_loc_result.txt加入到数据库中，why_tmp_event_loc_result（event_id,happen_area,happen_province,happen_city）
#把happen_province的不会则字段统一为，省、市、自治区
select happen_province,count(*) as cnt from why_tmp_event_loc_result group by happen_province
select happen_province from why_tmp_event_loc_result where happen_province in ('北京','上海','天津','重庆')
update why_tmp_event_loc_result set happen_province = concat(happen_province,'市') where happen_province in ('北京','上海','天津','重庆')
update why_tmp_event_loc_result set happen_province = concat(happen_province,'省') where happen_province in ('云南','四川','安徽','山东','山西','广东','广西','江苏','江西','河南','浙江','湖北','湖南','甘肃','福建','贵州','辽宁','陕西','青海','黑龙江')
update why_tmp_event_loc_result set happen_province = concat(happen_province,'古') where happen_province in ('内蒙')
update why_tmp_event_loc_result set happen_province = concat(happen_province,'自治区') where happen_province in ('新疆','宁夏','内蒙古')
#更新到event_attributes表中
UPDATE event_attributes ea, why_tmp_event_loc_result wtr SET
		ea.happen_area=wtr.happen_area,
        ea.happen_province=wtr.happen_province,
		ea.happen_city=wtr.happen_city
        WHERE ea.event_id = wtr.event_id;
drop table why_tmp_event_loc_result;

#把各城市gdp、各省gdp数据、各省人口数据、各省汉族人口比例数据上传
#创建3张表，city_gdp(city_gdp_ranking,city,2012_gdp,2013_gdp,gdp_increase_from_2012,in_province)/province_gdp(province_gdp_ranking_2013,province,province_gdp_2013)
#/avg_province_gdp(avg_province_gdp_ranking_2013,province,province_gdp_2013,province_pnum_2013,avg_province_gdp_2013,avg_province_gdpdolar_2013)
SELECT ea.happen_city,cd.* from event_attributes as ea,city_gdp as cd where ea.happen_city like concat('%',cd.city,'%')
UPDATE event_attributes ea, city_gdp cd SET
		ea.city_gdp_ranking=cd.city_gdp_ranking,
        ea.2012_gdp=cd.2012_gdp,
		ea.2013_gdp=cd.2013_gdp,
		ea.gdp_increase_from_2012=cd.gdp_increase_from_2012
        WHERE ea.happen_city like concat('%',cd.city,'%');

SELECT ea.happen_province,pg.* from event_attributes as ea,province_gdp as pg where ea.happen_province like concat('%',pg.province,'%')
UPDATE event_attributes ea, province_gdp pg SET
		ea.province_gdp_ranking_2013=pg.province_gdp_ranking_2013,
        ea.province_gdp_2013=pg.province_gdp_2013
        WHERE ea.happen_province like concat('%',pg.province,'%');

SELECT ea.happen_province,apg.* from event_attributes as ea,avg_province_gdp as apg where ea.happen_province like concat('%',apg.province,'%')
UPDATE event_attributes ea, avg_province_gdp apg SET
		ea.avg_province_gdp_ranking_2013=apg.avg_province_gdp_ranking_2013,
        ea.province_pnum_2013=apg.province_pnum_2013,
		ea.avg_province_gdp_2013=apg.avg_province_gdp_2013
        WHERE ea.happen_province like concat('%',apg.province,'%');


#创建少数民族人口比例表ratio_province(province,province_hanzu_ratio)
SELECT ea.happen_province,rp.* from event_attributes as ea,ratio_province as rp where ea.happen_province like concat('%',rp.province,'%')
UPDATE event_attributes ea, ratio_province rp SET
		ea.province_hanzu_ratio=rp.province_hanzu_ratio
        WHERE ea.happen_province like concat('%',rp.province,'%');


#小强的需求
select t.event_id,avg(pos_eval),avg(pos_emo),avg(pos_ntusd) from t_lable_filtered t,sentiment_news sn where t.id = sn.item_id group by t.event_id order by t.event_id

#富帅的需求
select ta.id,ea.happen_province from t_lable_filtered ta,event_attributes ea where ta.event_id = ea.event_id
UPDATE t_lable_filtered ta,event_attributes ea SET
		ta.happen_province=ea.happen_province
        WHERE ta.event_id = ea.event_id;



