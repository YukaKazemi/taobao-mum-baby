import datetime

import pandas as pd
import numpy as np
import matplotlib as mpt
from matplotlib import pyplot as plt

mpt.use('TkAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

trade_history = pd.read_csv(r'../data/new_trade_history.csv')
mum_baby_trade_history = pd.read_csv(r'../data/tianchi_mum_baby_trade_history.csv')

# 消费者行为分析
print(mum_baby_trade_history.groupby('category_1').sum())  # 查看根类别category_1 #[6 rows x 7 columns]
result1 = pd.pivot_table(mum_baby_trade_history, index='category_1', values='buy_mount', aggfunc=np.sum)
plt.figure(figsize=(7, 5))
plt.bar(x=['28', '38', '50008168', '50014815', '50022520', '122650008'],
        height=result1['buy_mount'])
plt.title("category_1类别销量")
plt.savefig('../tmp/消费者行为分析.svg')
plt.show()

# 由图可知，商品编号为28的销量最高，而50014815次之，而122650008的销量最低，应对此现状提高或减少生产量或者加大宣传力度。


# 不同性别用户的销售情况分析
data = pd.pivot_table(trade_history, index='gender', values='buy_mount', aggfunc=np.sum)
print(data)
plt.figure(figsize=(5, 5))
plt.pie(['718', '544', '43'],
        labels=['女', '男', '未知'],
        colors=['r', 'b', 'g'],
        autopct='%.2f%%')
plt.title("性别与购买数量的销售关系")
plt.savefig('../tmp/性别和购买数量的关系.svg')
plt.show()
# 由图可知，婴幼儿为女孩的销售量较女孩更大一些，而未出生购买商品的用户占比很小，所以应该加大用户家婴幼儿是女孩的推广力度以及产品制造。

# 不同性别购买商品种类的关系分析
data = pd.pivot_table(trade_history, index='category_1',
                      columns='gender',
                      values='buy_mount',
                      aggfunc=np.sum)
plt.figure(figsize=(12, 5))
plt.subplot(221)
# 男
plt.bar(x=['28', '38', '50008168', '50014815', '50022520', '122650008'],
        height=data[0], color='r')
plt.subplot(222)
# 女
plt.bar(x=['28', '38', '50008168', '50014815', '50022520', '122650008'],
        height=data[1], color='b')
plt.subplot(223)
# 未出生
plt.bar(x=['28', '38', '50008168', '50014815', '50022520', '122650008'],
        height=data[2], color='g')
plt.xlabel("商品种类")
plt.ylabel("销售数量")
plt.savefig('../tmp/不同性别购买商品种类的关系.svg')
plt.show()
# 由图可知，已出生婴幼儿对编号50008168商品需求量较大，婴幼儿女孩对编号50014815需求量高于男孩，，而未出生购买50014815最高其他商品需求偏低，应对此现状提高或减少生产量或者加大宣传力度。。


# 销量与月份关系分析
# 分析波峰：在每年的10到11月份左右会有一个大波峰，每年的5月以及9月左右会有一个小波峰，在这段时间销量较同期会有一个明显的涨幅
# 推测1：节日因素，在5月有劳动节，母亲节；9月有中秋节；而是10月到11月左右有国庆节、万圣节、立冬、感恩节等节日，平台在这些节日可能绘有促销打折，这时随着价格降低需求量会增加，同时销售量也会增加。
# 推测2：双十一打折力度高，淘宝双十一是从2009年开始便存在的大型购物促销狂欢日，而又伴随着即将到来的春节假期，顾客可能进行囤货，结合两个因素导致需求量大幅上升，所以在11月前会出现一个大型的销量波峰。
# 结论：在5月与9月以及11月需要加大供货量，保证供需平衡。

# 分析波谷：每年的1月左右会出现一个明显的销量波谷，说明这段时间的销量较同期低。
# 推测：1月份正值春节，店铺休息，而开着的店铺肯定会抬高物价，而用户在11月进行囤货所以导致1月份的需求量减小，出现销量波谷。
# 结论：1月销量惨淡，需要考虑减少进货量的问题，适当降低物价拓宽销售渠道加大宣传力度。

mum_baby_trade_history["day"] = mum_baby_trade_history['day'].apply(
    lambda x: datetime.datetime.strptime(str(x), "%Y%m%d"))
mum_baby_trade_history['Month'] = mum_baby_trade_history.day.astype('datetime64[M]')  # 设置成月份形式
print(mum_baby_trade_history)
data_month = mum_baby_trade_history.groupby('Month', as_index=False)  # 按月份分类
data_month.buy_mount.sum()  # 按月份汇总
df = data_month.buy_mount.sum()  # 新建汇总列表
plt.figure(figsize=(20, 5))
plt.plot(df["Month"], df["buy_mount"])
plt.savefig('../tmp/销量与月份走势图.svg')
plt.show()

