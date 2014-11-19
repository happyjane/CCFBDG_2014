# -*- coding: utf-8 -*-

import fileinput
# import numpy as np
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
from gensim import corpora, models, similarities

def cos(a, b):
	import math
	try:
		return sum([sa*sb if pa == pb else 0 for (pa,sa) in a for (pb,sb) in b])/math.sqrt(sum([sa**2 for (pa,sa) in a])*sum([sb**2 for (pb,sb) in b]))
	except:
		return 0

# 新闻分类
import time
import fileinput
A1 = ["公交","车辆","巴士","交通","乘坐","车厢","车窗","驾驶员","司机","乘客"]
A2 = ["爆炸","炸弹","起火","大火","燃烧","自燃"]
B1 = ["暴力","恐怖","暴徒","袭击","击毙","自杀式"]
C1 = ["校园","学校","高校","名校","校内","校外","小学","中学","初中","高中","大学","学生","同学","教师","老师","师生","幼儿园"]
C2 = ["砍","刀","匕首","刺","捅","杀"]
file1 = open("tag_pos_t_lable_group_comp_1.seg.txt","w")
file2 = open("tag_neg_t_lable_group_comp_1.seg.txt","w")
for line in fileinput.input("t_lable_group_comp_1.sort.seg.txt"):
	cid = line.strip().split("\t")[0][1:-1]
	day = (int(time.mktime(time.strptime(line.strip().split("\t")[1][1:-1],'%Y-%m-%d %H:%M:%S')))-int(time.mktime(time.strptime("2012-10-01 00:00:00",'%Y-%m-%d %H:%M:%S'))))/(24*3600)
	title = line.strip().split("\t")[4][1:-1].split(" ")
	content = line.strip().split("\t")[7][1:-1].split(" ")
	nr_map_t, ns_map_t = {}, {}
	for item in title:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"] and len(item.split("/")[0])/3>=2:
			nr_map_t[item.split("/")[0]] = 1 if not nr_map_t.has_key(item.split("/")[0]) else nr_map_t[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"] and len(item.split("/")[0])/3>=2:
			ns_map_t[item.split("/")[0]] = 1 if not ns_map_t.has_key(item.split("/")[0]) else ns_map_t[item.split("/")[0]]+1
	nr_map_c, ns_map_c = {}, {}
	for item in content:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"] and len(item.split("/")[0])/3>=2:
			nr_map_c[item.split("/")[0]] = 1 if not nr_map_c.has_key(item.split("/")[0]) else nr_map_c[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"] and len(item.split("/")[0])/3>=2:
			ns_map_c[item.split("/")[0]] = 1 if not ns_map_c.has_key(item.split("/")[0]) else ns_map_c[item.split("/")[0]]+1
	title_orig = "".join([item.split("/")[0] for item in title])
	s1 = sum([1 if w in title_orig else 0 for w in A1])
	s2 = sum([1 if w in title_orig else 0 for w in A2])
	s3 = sum([1 if w in title_orig else 0 for w in B1])
	s4 = sum([1 if w in title_orig else 0 for w in C1])
	s5 = sum([1 if w in title_orig else 0 for w in C2])
	tag = 0
	if s1 >= 1 and s2 >= 1:
		tag = 1
	if s3 >= 1:
		tag = 2
	if s4 >= 1 and s5 >= 1:
		tag = 3
	if tag != 0:
		# print tag, title_orig
		# print " ".join([k+":"+str(v) for k,v in nr_map_t.iteritems()])
		# print " ".join([k+":"+str(v) for k,v in ns_map_t.iteritems()])
		# print " ".join([k+":"+str(v) for k,v in nr_map_c.iteritems()])
		# print " ".join([k+":"+str(v) for k,v in ns_map_c.iteritems()])
		file1.write(cid+"\t"+str(tag)+"\t"+str(day)+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_c.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_c.iteritems()])+"\""+"\t"+title_orig+"\n")
	else:
		file2.write(line)
fileinput.close()
file1.close()
file2.close()

# 事件划分
documents, news = [], []
c = 0
for line in fileinput.input("tag_pos_t_lable_group_comp_1.seg.txt"):
	part = line.strip().split("\t")
	cid, cls, day = part[0], int(part[1]), int(part[2])
	title_nf = None if len(part[3][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[3][1:-1].split(" ")]
	title_ns = None if len(part[4][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[4][1:-1].split(" ")]
	content_nf = None if len(part[5][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5][1:-1].split(" ")]
	content_ns = None if len(part[6][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[6][1:-1].split(" ")]
	title = part[-1]
	news.append([cls, day, cid+"\t"+title+"\t"+part[3]+"|"+part[4]+"|"+part[5]+"|"+part[6]])
	text, weight = [], 5
	if title_nf != None:
		for w in title_nf:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if title_ns != None:
		for w in title_ns:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if content_nf != None:
		for w in content_nf:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	if content_ns != None:
		for w in content_ns:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	documents.append(" ".join(text).encode("utf-8"))
	c += 1
fileinput.close()
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
print len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
event = {1:[],2:[],3:[]}
c = 0
for doc in corpus_tfidf:
	print c
	feature = doc
	maxsim, assign = 0, -1
	for e in xrange(len(event[news[c][0]])):
		if abs(event[news[c][0]][e]["stime"] - news[c][1]) <= 14:
			sim = cos(event[news[c][0]][e]["feature"],feature)
			# print "---- ---- ----"
			# print event[news[c][0]][e]["title"][0], news[c][2], sim
			# print event[news[c][0]][e]["feature"], feature
			# print "---- ---- ----"
			if sim > maxsim:
				maxsim, assign = sim, e
	# print maxsim
	if maxsim >= 0.15:
		event[news[c][0]][assign]["title"].append(news[c][2])
		fmap = {}
		for (p,s) in event[news[c][0]][assign]["feature"]:
			fmap[p] = s
		for (p,s) in feature:
			fmap[p] = s if not fmap.has_key(p) else fmap[p]+s
		event[news[c][0]][assign]["feature"] = [(p,s) for p,s in fmap.iteritems()]
	else:
		event[news[c][0]].append({"stime":news[c][1],"feature":feature,"title":[news[c][2]]})
	c += 1
file = open("classified_news.txt","w")
c = 0
for i in [1,2,3]:
	for e in event[i]:
		for t in e["title"]:
			file.write(str(c)+"\t"+str(i)+"\t"+str(e["stime"])+"\t"+t+"\n")
		c += 1
file.close()

documents = ["Shipment of gold damaged in a fire","Delivery of silver arrived in a silver truck","Shipment of gold arrived in a truck"]
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
	print doc

# 微博分类
import time
import fileinput
A1 = ["公交","车辆","巴士","交通","乘坐","车厢","车窗","驾驶员","司机","乘客"]
A2 = ["爆炸","炸弹","起火","大火","燃烧","自燃"]
B1 = ["暴力","恐怖","暴徒","袭击","击毙","自杀式"]
C1 = ["校园","学校","高校","名校","校内","校外","小学","中学","初中","高中","大学","学生","同学","教师","老师","师生","幼儿园"]
C2 = ["砍","刀","匕首","刺","捅","杀"]
event_map = {}
for line in fileinput.input("data/classified_news.txt"):
	part = line.strip().split("\t")
	event, cls, day = int(part[0]), int(part[1]), int(part[2])
	nr_t = None if len(part[5].split("|")[0][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[0][1:-1].split(" ")]
	ns_t = None if len(part[5].split("|")[1][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[1][1:-1].split(" ")]
	nr_c = None if len(part[5].split("|")[2][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[2][1:-1].split(" ")]
	ns_c = None if len(part[5].split("|")[3][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[3][1:-1].split(" ")]
	text, weight = [], 5
	if nr_t != None:
		for w in nr_t:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if ns_t != None:
		for w in ns_t:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if nr_c != None:
		for w in nr_c:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	if ns_c != None:
		for w in ns_c:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	if not event_map.has_key(event):
		event_map[event] = {"cls":cls,"stime":day,"text":text}
	else:
		event_map[event]["text"].extend(text)
fileinput.close()
documents = []
for k, v in event_map.iteritems():
	documents.append(" ".join(v["text"]).encode("utf-8"))
weibo = []
for line in fileinput.input("data/t_lable_group_comp_4.sort.seg.txt"):
	cid = line.strip().split("\t")[0][1:-1]
	day = (int(time.mktime(time.strptime(line.strip().split("\t")[1][1:-1],'%Y-%m-%d %H:%M:%S')))-int(time.mktime(time.strptime("2012-10-01 00:00:00",'%Y-%m-%d %H:%M:%S'))))/(24*3600)
	content = line.strip().split("\t")[5][1:-1].split(" ")
	nr_map_t, ns_map_t = {}, {}
	for item in content:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"]:
			nr_map_t[item.split("/")[0]] = 1 if not nr_map_t.has_key(item.split("/")[0]) else nr_map_t[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"]:
			ns_map_t[item.split("/")[0]] = 1 if not ns_map_t.has_key(item.split("/")[0]) else ns_map_t[item.split("/")[0]]+1
	text = []
	for k,v in nr_map_t.iteritems():
		try:
			text.extend([k.decode("utf-8")]*v)
		except:
			continue
	for k,v in ns_map_t.iteritems():
		try:
			text.extend([k.decode("utf-8")]*v)
		except:
			continue
	content_orig = "".join([item.split("/")[0] for item in content])
	s1 = sum([1 if w in content_orig else 0 for w in A1])
	s2 = sum([1 if w in content_orig else 0 for w in A2])
	s3 = sum([1 if w in content_orig else 0 for w in B1])
	s4 = sum([1 if w in content_orig else 0 for w in C1])
	s5 = sum([1 if w in content_orig else 0 for w in C2])
	cls = 0
	if s1 >= 1 and s2 >= 1:
		cls = 1
	if s3 >= 1:
		cls = 2
	if s4 >= 1 and s5 >= 1:
		cls = 3
	if cls != 0:
		documents.append(" ".join(text).encode("utf-8"))
		weibo.append({"cid":cid,"cls":cls,"day":day,"content":content_orig})
fileinput.close()
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
print len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
file = open("data/classified_weibo.txt","w")
c = 0
for doc in corpus_tfidf:
	print c
	if c < len(event_map.keys()):
		event_map[c]["feature"] = doc
	else:
		maxsim, assign = 0, -1
		for k, v in event_map.iteritems():
			if weibo[c-len(event_map.keys())]["cls"] == v["cls"] and 0 <= day - v["stime"] <= 28:
				sim = cos(v["feature"],doc)
				if sim > maxsim:
					maxsim, assign = sim, k
		print maxsim
		if maxsim >= 0.15:
			file.write(str(assign)+"\t"+str(weibo[c-len(event_map.keys())]["cls"])+"\t"+str(weibo[c-len(event_map.keys())]["day"])+"\t"+weibo[c-len(event_map.keys())]["cid"]+"\t"+weibo[c-len(event_map.keys())]["content"]+"\n")
	c += 1
file.close()

emap = {1:{},2:{},3:{}}
for line in fileinput.input("data/classified_news.txt"):
	part = line.strip().split("\t")
	e, c, d = int(part[0]), int(part[1]), int(part[2])
	if not emap[c].has_key(e):
		emap[c][e] = {"news":[d],"weibo":[]}
	else:
		emap[c][e]["news"].append(d)
fileinput.close()
for line in fileinput.input("data/classified_weibo.txt"):
	part = line.strip().split("\t")
	e, c, d = int(part[0]), int(part[1]), int(part[2])
	emap[c][e]["weibo"].append(d)
fileinput.close()
import matplotlib.pyplot as plt
for k,v in emap.iteritems():
	l1, l2, l3 = [0,1125], [0,1125], [0,1125]
	for e,r in v.iteritems():
		l1.append(min(r["news"]))
		l2.extend(r["news"])
		l3.extend(r["weibo"])
	fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 4))
	ax0.hist(l1, 500, normed=1, histtype='bar', facecolor='r', alpha=0.75)
	ax0.set_title('type '+str(k)+' event density')
	ax1.hist(l2, 500, normed=1, histtype='stepfilled', facecolor='g', rwidth=0.8)
	ax1.set_title('type '+str(k)+' webnews density')
	ax2.hist(l3, 500, normed=1, histtype='stepfilled', facecolor='b', rwidth=0.8)
	ax2.set_title('type '+str(k)+' sinaweibo density')
	plt.tight_layout()
	plt.show()

n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
# add a 'best fit' line
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y, 'r--')

