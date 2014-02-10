from sets import Set
def all_url(filename):
	urls = Set()
	with open(filename) as fp:
		for line in fp:
			line = line.replace('\n','')
			line = line.split('\t')
			for item in line:
				if item not in urls:
					urls.add(item)
	return urls

if __name__ == '__main__':
	result = all_url("topic_urls.txt")
	for line in result:
		print line
