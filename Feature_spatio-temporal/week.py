if __name__ == "__main__":
	f = open('../1/ttl_result.txt','r')
	matrix = []
	i = 0
	for lines in f.read().split('\n'):
		matrix.append(int(lines.split('\t')[1]) % 7)
		# print int(lines.split('\t')[2]) % 7
	fw = open ('week_result.txt','w')
	j = 0
	for k in matrix:
		fw.write(str(j))
		fw.write('\t')
		if k == 1:
			fw.write('Monday')
		elif k == 2:
			fw.write('Tuesday')
		elif k == 3:
			fw.write('Wednesday')
		elif k == 4:
			fw.write('Thursday')
		elif k == 5:
			fw.write('Friday')
		elif k == 6:
			fw.write('Saturday')
		elif k == 0:
			fw.write('Sunday')
		fw.write('\n')	
		j = j+1