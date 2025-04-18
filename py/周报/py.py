import os

f1 = open("./a.txt",'r')
f2 = open('./b.txt','w')
text = f1.read()
list = text.split(' ')
for i in list:
	f2.write(i+'、')
	print(i)
f2.close()
