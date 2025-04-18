from lxml import etree
import datetime

start = int(input('开始时间：(eq:20240824)'))
end = int(input('结束时间：'))

items = []
dateList = {}

f = open('./out_files/ifr.html','r',encoding='utf-8')
html = f.read()

# 创建一个XPath解析对象，用于解析HTML数据
tree = etree.HTML(html)

# 使用XPath语法提取指定标签及其内容  //*[@id="activity-stream"]/div[18]  //*[@id="activity-stream"]/div[5]/div[1]/a[2]/span
tag = tree.xpath('//*[@id="activity-stream"]/div')
# print(len(tag))
for i in tag:
    if i.xpath('./@class')[0] == 'date-header':
        continue
    items.append(i)
    # print(i.xpath('//div[@class="activity-item-summary"]/text()'))
    for j in i.xpath('./div[@class="activity-item-summary"]/text()'):
        if "解决结果： '已解决" in j:
            time = datetime.datetime.strptime(i.xpath('./div[@class="activity-item-info"]/span')[0].text,'%Y/%m/%d %H:%M:%S').date()
            # print(i.xpath('./div[@class="activity-item-info"]/span')[0].text)
            list = dateList.get(str(time).replace('-',''))
            if not list:
                list = []
            list.append(i.xpath('./div[@class="activity-item-summary"]/a[2]/span/text()')[0])
            # print(i.xpath('./div[@class="activity-item-summary"]/a[2]/span/text()')[0])
            dateList[str(time).replace('-','')] = list
            break
keys = dateList.keys()
keys = sorted(keys)
out = ''
with open("./out.txt",'w',encoding="utf-8") as f:
    for k in keys:
        # print(k)
        # print(*dateList[k],sep='、')
        if int(k) < start:
            continue
        if int(k) > end:
            break
        f.write(k + '\n')
        f.write('、'.join(dateList[k]))
        out += '、'.join(dateList[k]) + '、'
        f.write("\n")
    f.write(f"总结：{out}")

