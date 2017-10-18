# -*- coding：utf-8 -*-

import os

#写入文件
f=open("output_task_credit.txt","w")

task=[]#纬度，经度，价格，完成情况
user_cre=[]#纬度，经度, 信誉

#读入文件
for line in open("task_com.txt","r").readlines():
    #保存一个空格连接
    result1=' '.join(line.split())
    #获取每行值
    s1=[float(x) for x in result1.strip().split(' ')]
    #数据存储到dtask
    task.append(s1)

for line in open("user_credit.txt","r").readlines():
    #保存一个空格连接
    result2=' '.join(line.split())
    #获取每行值
    s2=[float(x) for x in result2.strip().split(' ')]
    #数据存储到user
    user_cre.append(s2)

from math import radians, cos, sin, asin, sqrt,fabs
def hav(theta):
    s=sin(theta/2)
    return s*s
def dis(lon1,lat1,lon2,lat2):#经度1，纬度1

    #十进制转化为弧度
    lon1,lat1,lon2,lat2 = map(radians,[lon1,lat1,lon2,lat2])
    #haversine公式
    dlon=fabs(lon2-lon1)
    dlat=fabs(lat2-lat1)
    h=hav(dlat)+cos(lat1)*cos(lat2)*hav(dlon)
    r=6371  #地球半径
    distance=2*r*asin(sqrt(h))    #千米
    return distance

task_com=[]#标号，价格，完成情况，7km内信誉均值

#遍历task，找出7KM内用户信誉值均值
i=0
for x in task:
    total_cre=0
    n=0
    a = []#一条任务信息
    a.append(i)#任务标号
    a.append(x[2])#价格
    a.append(x[3])#完成情况

    for y in user_cre:
        distance = dis(x[1], x[0], y[1], y[0])
        if (distance < 7):
            total_cre+=y[2]
            n+=1
    if n==0:
        average=0
    else:
        average=total_cre/n
    a.append(average)#信誉均值
    task_com.append(a)
    i+=1

print("任务序号 价格 完成情况 7km内用户信誉均值", file=f)
i=0
for x in task_com:
        print(x[0], end=' ', file=f)
        print(x[1], end=' ', file=f)
        print(x[2], end=' ', file=f)
        print(x[3],end=' ',file=f)
        print('',file=f)

f.close()
