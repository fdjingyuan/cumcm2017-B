# -*- coding：utf-8 -*-

import os

#写入文件
f=open("output_task_user.txt","w")

task=[]#纬度，经度，价格
user=[]#纬度，经度
for line in open("task.txt","r").readlines():
    #保存一个空格连接
    result1=' '.join(line.split())
    #获取每行值
    s1=[float(x) for x in result1.strip().split(' ')]
    #数据存储到dtask
    task.append(s1)

for line in open("user.txt","r").readlines():
    #保存一个空格连接
    result2=' '.join(line.split())
    #获取每行值
    s2=[float(x) for x in result2.strip().split(' ')]
    #数据存储到user
    user.append(s2)

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

#遍历task，计算用户密集度

k_test=1
while k_test<20:
    num = 0
    data = [[65, 0, []], [65.5, 0, []], [66, 0, []], [66.5, 0, []], [67, 0, []], [67.5, 0, []], [68, 0, []], [68.5, 0, []], [69, 0, []], [69.5, 0, []], [70, 0, []], \
            [70.5, 0, []], [71, 0, []], [71.5, 0, []], [72, 0, []], [72.5, 0, []], [73, 0, []], [73.5, 0, []],[74, 0, []], [74.5, 0, []], [75, 0, []], [80, 0, []], [85, 0, []]]

    for x in task:
        k=int(x[2]*2)
        if x[2]==80:
            data[21][1]+=1
        elif x[2]==85:
            data[22][1]+=1
        else:
            data[k-130][1]+=1

        n=0
        for y in user:
            distance=dis(x[1],x[0],y[1],y[0])
            if (distance< k_test):
                n+=1
            num+=1

        k=int(x[2]*2)
        if x[2]==80:
            data[21][2].append(n)
        elif x[2]==85:
            data[22][2].append(n)
        else:
            data[k-130][2].append(n)


    #计算次数
    print(num)
    #对不同价格的任务用户数排序
    print("价格 任务数 对应任务在%d km内的用户数"%k_test,file=f)
    for x in data:
        x[2]=sorted(x[2])
        print(x[0], end=' ', file=f)
        print(x[1], end=' ', file=f)
        for y in x[2]:
            print(y, end=' ',file=f)
        print('',file=f)

    k_test+=1






