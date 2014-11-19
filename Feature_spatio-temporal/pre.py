if __name__ == "__main__":
	f = open('holiday.txt','r')
	fw = open('holiday_mod.txt','w')
	for lines in f.read().split('\n'):
		fw.write(lines.split('\t')[0]+'\t')
		k = len (lines.split('\t'))
		print k
		for i in range(1,k):
			fw.write(str(549+int(lines.split('\t')[i]))+'\t')
		fw.write('\n')
