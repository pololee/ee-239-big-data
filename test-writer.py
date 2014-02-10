import time
fw = open("test-writer.txt", mode='w')
for x in range(10):
	 fw.write("polo\n")
time.sleep(1500)
