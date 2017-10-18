"""
可视化绘图

"""
import os
import numpy as np
import matplotlib.pyplot as plt

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

#获取第一列和第二列数据
tx=[n[0] for n in task]
ty=[n[1] for n in task]

ux=[n[0] for n in user]
uy=[n[1] for n in user]

#绘制散点图


plt.xlim(xmax=114.5,xmin=112.6)
plt.ylim(ymax=23.7,ymin=22.4)
#四个颜色：红 绿 蓝 黄
plot1, = plt.plot(ty,tx,'or',marker="o",markersize=5)
plot2, = plt.plot(uy,ux,'og',marker="o",markersize=3)


#标题
plt.title("distribution of users and tasks ")

#x和y轴坐标
plt.xlabel("longitude")
plt.ylabel("latitude")

#图例
plt.legend((plot1,plot2),('task','user'),fontsize=10)
plt.show()

