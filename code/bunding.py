# -*- coding：utf-8 -*-

import os

#写入文件
f1=open("output_bunding_user.txt","w")
f2=open("output_bunding.txt","w")

user=[]#编号，纬度，经度，预定限额，开始时间，信誉值，实际限额
task=[]#编号，纬度，经度，价格
result=[]#输出结果 任务数 价格 单位任务路径

#读入文件
for line in open("task_order.txt","r").readlines():
    #保存一个空格连接
    result1=' '.join(line.split())
    #获取每行值
    s1=[x for x in result1.strip().split(' ')]
    #数据存储到task
    task.append(s1)

for line in open("user_order.txt","r").readlines():
    #保存一个空格连接
    result2=' '.join(line.split())
    #获取每行值
    s2=[x for x in result2.strip().split(' ')]
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

#计算7km内用户人数和信誉均值
tnum=[]
dist=[]
cred=[]
for x in task:
    ndist=0
    ncred=0
    tnum.append(x[0])
    for y in user:
        distance = dis(float(x[2]), float(x[1]), float(y[2]), float(y[1]))
        if(distance<7):
            ndist+=1
            ncred+=float(y[5])
    dist.append(ndist)
    cred.append(ncred)

dic_d=dict(zip(tnum,dist))
dic_c=dict(zip(tnum,cred))


total_user=[]
i=0
for x in user:
    s=[]
    tasknum=int(x[6])
    for y in task:
        point = []  # 2km内任务编号，距离
        if(tasknum==0 or tasknum==1):
            break
        distance = dis(float(x[2]), float(x[1]), float(y[2]), float(y[1]))
        if(distance<2):
            point.append(y[0])
            point.append(distance)
            point.append(y[3])
            s.append(point)#用户

    sorted(s, key=lambda s: s[1])#按距离排序
    if(len(s) > tasknum):#2km内任务比限额大,取限额数内最近的一些未打包的任务打包
        s=s[:tasknum:1]
    elif(len(s)==1):#一个任务不能打包
        s=[]

    s.insert(0,user[i][0])#用户编号,打包[任务编号，距离,价格]
    total_user.append(s)

    #删除已打包的任务
    task_bunding = []#打包的编号
    total_price=0
    total_cred=0
    total_num=0
    for a in task:
        for b in s:
            if(a[0]==b[0]):
                task.remove(a)
                total_price+=int(float(a[3]))
                task_bunding.append(a[0])#加入打包任务组
    if(task_bunding!=[]):
        t=0
        while(t<len(task_bunding)):
            total_cred+=dic_c[task_bunding[t]]
            total_num+=dic_d[task_bunding[t]]
            t+=1
        aver_num=total_num/len(task_bunding)
        aver_cre = total_cred / len(task_bunding)
        temp=[len(task_bunding),task_bunding,round(total_price/len(task_bunding),1),aver_num, aver_cre]
        result.append(temp)
    i+=1



print("任务数 价格 平均用户密度 平均信誉值 任务编号  ",file=f2)
for x in result:
    print(x[0],end=' ',file=f2)
    print(((x[2]+0.25)//0.5)*0.5,end=' ',file=f2)
    print(int(x[3]), end=' ', file=f2)
    print(x[4], end=' ', file=f2)
    for y in x[1]:
        print(y,end=' ',file=f2)
    print('',file=f2)

for x in task:
    print("1",end=' ',file=f2)
    print(((float(x[3])+0.25)//0.5)*0.5, end=' ', file=f2)
    print(int(dic_d[x[0]]),end=' ',file=f2)
    print(dic_c[x[0]],end=' ',file=f2)
    print(x[0], file=f2)



print("用户打包信息：用户编号，[打包任务编号，距离，价格]",file=f1)
for x in total_user:
    for y in x:
        print(y,end=' ',file=f1)
    print('',file=f1)


