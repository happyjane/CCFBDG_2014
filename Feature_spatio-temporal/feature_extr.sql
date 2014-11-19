一、表与字段的说明
1.原始表
t_lable_group_comp：3年（2011-10-01~~2014-04-30）的微博和资讯数据, 364924条记录(36万)
t_dpt_comp：咨询的转发量和评论量等数据,	257550条记录（25万）
w_user_info_comp：相应微博人物资料数据

t_lable_group_comp表中的url_crc对应t_dpt表中的url_crc相对应
t_lable_group_comp表中的siteurl_crc对应w_user_info_comp中的url_crc
2.处理后的表

二、其他说明
1.各个事件打的标签：
（1）公交车爆炸事件数据（某市公交车爆炸案等）
（2）暴恐事件数据（如某地暴恐事件、某地火车站暴恐事件等）
（3）校园砍伤事件数据

三、特征提取工作
1.空间特征
（1）新闻关注者的地理空间分布（wb_loc_num）
（2）事件发生地的经济发达程度，可按近几年的省级GDP排名
（3）事件发生地的行政级别：如县、市、区
2.媒体特征
（1）事件微博上的关注次数（wb_cnt_num）
（2）事件微博上的关注人数（wb_person_num）
（3）事件微博上的重复关注次数（wb_repeat_num）

四、SQL代码
#提取出某事件微博上的关注次数、关注人数、重复关注次数、关注地点数
select t.event_id,COUNT(w.url_crc) as wb_cnt_num,count(DISTINCT w.url_crc) as wb_person_num,(COUNT(w.url_crc)-count(DISTINCT w.url_crc)) as wb_repeat_num,count(DISTINCT w.location) as wb_loc_num from t_lable_filtered as t inner JOIN w_user_info_distinct as w on t.siteurl_crc=w.url_crc  GROUP BY event_id order by t.event_id


#把结果更新到event_attributes中
UPDATE event_attributes e, event_tmp_why ew SET
		e.wb_cnt_num=ew.wb_cnt_num,
        e.wb_person_num=ew.wb_person_num,
		e.wb_repeat_num=ew.wb_repeat_num,
		e.wb_loc_num=ew.wb_loc_num
        WHERE e.event_id = ew.event_id;
drop table event_tmp_why;


#抽取出重复的url_crc
select distinct a.url_crc from w_user_info_distinct as a,(select url_crc,count(1) as ct from w_user_info_distinct group by url_crc order by ct desc) as b where a.url_crc=b.url_crc and b.ct>1 order by url_crc
#在表w_user_info_distinct中添加一列主键
alter table w_user_info_distinct add column id int not null auto_increment primary key comment 'primary key' first;
#删除重复的url_crc
delete from w_user_info_distinct WHERE url_crc in (select * from w_user_dist_url_crc) and id%2=1
#删除id列
alter table w_user_info_distinct drop column id

SELECT ea.happen_city,cd.* from event_attributes as ea,city_gdp as cd where ea.happen_city like concat('%',cd.city,'%')
