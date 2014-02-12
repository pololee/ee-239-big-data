def pass_by_what(ss):
	print ss
	ss.append(100)

def play():
	li = [1,2,3,4]
	pass_by_what(li)
	print li

if __name__ == '__main__':
	play()