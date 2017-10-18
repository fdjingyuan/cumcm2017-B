# -*- coding：utf-8 -*-

import os
import random

#写入文件
f=open("output_intimate.txt","w")

prop=[]#十个区间概率值

for line in open("intimate.txt","r").readlines():
    #保存一个空格连接
    result1=' '.join(line.split())
    #获取每行值
    s2=[int(float(x)) for x in result1.strip().split(' ')]
    #数据存储到dtask
    prop.append(s2)


total=[30,194,233,175,371,236,286,206,229,106]
n=0
for x in prop:
    s = []
    m=0
    for y in x:
        num=y
        i=0
        while(i<num):
            s.append(int(m*0.5+65))
            i+=1
        m+=1

    if(len(s)<total[n]):
        k=total[n]-len(s)
        b=0
        while(b<k):
            s.append(random.randint(0,20)*0.5+65)
            b=b+1

    n+=1

    random.shuffle(s)
    for x in s:
        print(x,file=f)


f.close()
