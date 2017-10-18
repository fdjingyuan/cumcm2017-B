# -*- coding：utf-8 -*-

import os

#写入文件
f=open("output_price_distribution.txt","w")

price=[]

#读入文件
for line in open("price.txt","r").readlines():
    #保存一个空格连接
    result1=' '.join(line.split())
    #获取每行值
    s=[float(x) for x in result1.strip().split(' ')]
    #数据存储到price
    price.append(s)

distribution=[]
i=0
while i< 21:
    s=[price[i][0],0,0,0,0,0,0,0,0,0,0]#价格，人数……
    distribution.append(s)
    i+=1


j=0#价格65-75
for x in price:
    i=0#从第三列数据开始遍历
    for y in x:
        if i>1:
            if (y>=0 and y<=19):
                distribution[j][1]+=1
            elif(y>=20 and y<=39):
                distribution[j][2] += 1
            elif(y>=40 and y<=59):
                distribution[j][3] += 1
            elif(y>=60 and y<=79):
                distribution[j][4] += 1
            elif(y>=80 and y<=99):
                distribution[j][5] += 1
            elif(y>=100 and y<=119):
                distribution[j][6] += 1
            elif(y>=120 and y<=139):
                distribution[j][7] += 1
            elif(y>=140 and y<=159):
                distribution[j][8] += 1
            elif(y>=160 and y<=179):
                distribution[j][9] += 1
            elif(y>=180 and y<=199):
                distribution[j][10] += 1
        i+=1
    j+=1


print("价格\区间",file=f)

for x in distribution:
    for y in x:
        print(y,end=' ',file=f)
    print('', file=f)


f.close()