# cumcm2017-B
2017 problem B at China Undergraduate Mathematical Contest in Modeling 

There are some codes in our analysising process and the final thesis about our works.


支持文件列表
一．	Code文件夹
注：.py代码需要与txt文件放在同一文件夹中
1.	xgboost for problem 1-4.r:首先训练了判断任务完成度的xgboost模型，其次建立了第二问的基于xgboost 非线性整数规划问题求解的启发式算法代码；并计算了任务打包组合后定价后的任务完成情况；最后，建立了问题4的定价的PhaseII部分的代码。
2.	user-task.py：针对不同价格计算对应的任务数、在一定范围内对应的会员数
task.txt：输入文件，每列含义——附件一任务纬度 经度
user.txt：输入文件，每列含义——附件二会员纬度 经度
output_task_user.txt：输出文件，每列含义——价格 任务数 对应任务在x km内用户数，0<x<20，x为整数
3.	credit-task.py：计算任务周围用户密度
task_com.txt：输入文件，每列含义——附件一任务纬度 经度 价格 完成情况
user_credit.txt：输入文件，每列含义——附件二会员纬度 经度 信誉度
out_task_credit.txt：输出文件，每列含义——任务序号 价格 完成情况 7km内用户信誉均值
4.	price_distribution.py：计算对不同价格，在从0-199以20划分的区间中的概率数
price.txt：输入文件，每行含义——价格 对应任务数 每个任务在7km范围内会员数
output_price_distribution.txt：输出文件，每行含义——价格 在从0-199以20划分的区间中的会员数
5.	bunding.py：对附件一中的任务进行打包定价
task_order.txt：输入文件，每列含义——任务编码 纬度 经度
user_order.txt：输入文件，每列含义——会员编码 纬度 经度 限额 开始时间 信誉度
output_bunding_user.txt：输出文件，每列含义——会员编码 打包信息：[打包任务编号，距离，价格]
output_bunding.txt：输出文件，每列含义——用户编号 打包信息：[打包任务编号，距离，价格]
6.	intimate.py：依据概率模型，模拟出附件三新项目的原定价格
intimate.txt：输入文件，由概率模型得出的概率分布
output_intimate.txt：输出文件，按照7km范围内会员人数从小到大对应的模拟价格，也生成了问题4中定价的PhaseI部分的代码。
7.	new_user_task.py：附件三新文件不同价格在7km范围内的会员数
task_new.txt：输入文件，每列含义——附件三任务纬度 经度
output_new_task_user.txt：输出文件，每列含义——附件三任务纬度 经度 对应任务在7 km内的用户数
8.	figure.py：画出用户和任务分布散点图
9.	.idea：代码工程支持文件
二．数据整理 文件
1.  1-1题1-20km回归详细.xlsx
2.  1-1题价格分布.xlsx
3.  1-2题任务信誉情况.xlsx
4.  3题打包情况.xlsx
5.  4题模拟.xlsx
6.  task info.csv :用于R语言，第一题、第二题的xgboost的训练
7.  problem 3.csv：储存了py代码导出的定价和密度、信誉均值特征，用于r语言做预测
8.  problem_4_Phase_I.csv：储存了py生成的问题4中PhaseI的结果，用于R中PhaseII的初始化
9.member info.csv:用于R语言，第一问、第四问中提取任务与用户的交互特征的原始数据。


