import re
count = int(input('个数：'))
sids = open('./sid.txt','r')
out = open('./out.txt','w')
sid = sids.read()
outText = re.sub('\n',f',{count}|',sid) + f',{count}'
out.write(outText)
out.close()
print(1)
