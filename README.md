# 淘宝母婴购物数据可视化分析
## 数据集概述
数据集是阿里云天池的数据集:淘宝母婴购物数据的两个csv文件。  
[tianchi_mum_baby.csv](https://github.com/YukaKazemi/taobao-mum-baby/blob/master/data/tianchi_mum_baby.csv)  
[tianchi_mum_baby_trade_history.csv](https://github.com/YukaKazemi/taobao-mum-baby/blob/master/data/tianchi_mum_baby_trade_history.csv)  
包含了953个孩子的的生日和性别数据和29971条淘宝用户的历史交易数据。   
1. tianchi_mum_baby.csv  

| 列 | 描述 |
| ------ | ------ |  
| user_id | 用户 ID (Bigint). |  
| birthday | Children’s birthday (e.g. 20130423). |  
| gender | Children’s gender (“0” 女, “1” 男, “2” 未知). |  

2. tianchi_mum_baby_trade_history.csv

| 列 | 描述 |
| ------ | ------ |  
|  | ID (Bigint). |  
| user_id | 用户ID (Bigint). |  
| auction_id | 购买行为编号ID (Bigint). |
| category_2 | Category ID (Bigint). 类别ID |
| category_1 | Root category ID (Bigint). 根类别ID |
| buy_mount | Purchase quantity (Bigint). 采购量 |
| day | Timestamp. |    
  
3. 分析方向  
+什么商品类别销量最佳？  
+用户为之购买商品的婴儿年龄、性别分布？  
+销量与月份关系?

## 数据预处理  
以时间段较长的奶粉为例.  
对配方奶粉的分段，主要是根据国际食品法典委员会制定的cac来进行划分。  
婴幼儿奶粉现在大范围上基本分为一段、二段、三段，部分婴幼儿奶粉可能会分为四段、五段。  
奶粉分段及适用年龄：   
第1段婴幼儿奶粉适合0-6个月的宝宝；  
第2段婴幼儿奶粉适合6-12个月的宝宝；  
第3段婴幼儿奶粉适合1周岁-3周岁的宝宝；  
第4段奶粉适合3周岁-7周岁的孩子。  
7周岁最多为365*7=2555天，那么对于天数大于2560天的天数视为无效数据，删除行  
```  python
import pandas as pd

# 以时间段较长的奶粉为例.
# 配方奶粉的分段，主要是根据国际食品法典委员会制定的cac来进行划分。
# 婴幼儿奶粉现在大范围上基本分为一段、二段、三段，部分婴幼儿奶粉可能会分为四段、五段。
# 奶粉分段及适用年龄：
# 第1段婴幼儿奶粉适合0~6个月的宝宝；
# 第2段婴幼儿奶粉适合6~12个月的宝宝；
# 第3段婴幼儿奶粉适合1周岁~3周岁的宝宝；
# 第4段奶粉适合3周岁~7周岁的孩子。
# 7周岁最多为365*7=2555天，那么对于天数大于2560天的天数视为无效数据，删除行。


mum_baby = pd.read_csv('../data/tianchi_mum_baby.csv')
trade_history = pd.read_csv('../data/tianchi_mum_baby_trade_history.csv')

# 计算订单产生时小孩的天数
# 匹配mum_baby中user_id对应的trade_history的user_id
tample = mum_baby.merge(trade_history, how="left", on='user_id').fillna(0)
tample['birthday'] = pd.to_datetime(tample['birthday'].astype(str))
tample['day'] = pd.to_datetime(tample['day'].astype(str))
age_days = tample['day'] - tample['birthday']
tample.loc[:, 'age_days'] = age_days  # 计算订单产生时小孩的天数
print(tample.age_days)

j = 0
for i in age_days:
    tample.loc[j, 'age_days'] = i.days
    j += 1
# age_days为object类型  要改为int类型  不然describe无法统计年龄天数的最值
tample.age_days = pd.DataFrame(tample.age_days, dtype=int)

# 对于age的天数负数以及最大天数为10326天、购买数量最大值达到160天，可以做处理，也可以认为是正常数据不做处理
tample[tample['age_days'] > 2560].sort_values('age_days').to_excel(r'../data\age_days_gt7year.xlsx')
tample[tample['age_days'] < 0].sort_values('age_days').to_excel(r'../data/age_days_lt0year.xlsx')
print(tample[tample['age_days'] < 0].describe())
# 一般认为怀孕了再准备母婴用品会比较常见 这里 我们就以-300天(10个月)以上为正常  去掉低于-300天的购买数据
print(tample[tample['age_days'] > 2560])  # 一共24行
print(tample[tample['age_days'] < 0])  # 143行
print(tample[tample['age_days'] > 2560].index)
tample.drop(tample[tample['age_days'] > 2560].index, inplace=True)  # 删除大于2560天的行 在原始对象上修改
tample.drop(tample[tample['age_days'] < -300].index, inplace=True)  # 删除低于-300天的行
# 查看购买数量   七七八八的加起来50以内还算正常   达到160偏差有点不一般  还是删了吧

tample.drop(tample[tample['buy_mount'] > 50].index, inplace=True)
print(tample.describe())
tample.to_csv(r'../data/new_trade_history.csv')

```
## 数据可视化   
1. 消费者行为分析
   ``` python
   # 消费者行为分析
   print(mum_baby_trade_history.groupby('category_1').sum())  # 查看根类别category_1 #[6 rows x 7 columns]
   result1 = pd.pivot_table(mum_baby_trade_history, index='category_1', values='buy_mount', aggfunc=np.sum)
   plt.figure(figsize=(7, 5))
   plt.bar(x=['28', '38', '50008168', '50014815', '50022520', '122650008'],
        height=result1['buy_mount'])
   plt.title("category_1类别销量")
   plt.show()
   
   ```

   ![消费者行为分析图](https://raw.githubusercontent.com/YukaKazemi/taobao-mum-baby/cb8b7eeafcb952a93efe45843f5d3a381bd69e3d/tmp/%E6%B6%88%E8%B4%B9%E8%80%85%E8%A1%8C%E4%B8%BA%E5%88%86%E6%9E%90.svg)
   由图可知，商品编号为28的销量最高，而50014815次之，而122650008的销量最低，应对此现状提高或减少生产量或者加大宣传力度。
   
3. 不同性别用户的销售情况
   ``` python
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
   ```

   ![不同性别用户的销售情况分析](https://raw.githubusercontent.com/YukaKazemi/taobao-mum-baby/836c1644490ea6d0cce8b3febc852be88ba5415e/tmp/%E6%80%A7%E5%88%AB%E5%92%8C%E8%B4%AD%E4%B9%B0%E6%95%B0%E9%87%8F%E7%9A%84%E5%85%B3%E7%B3%BB.svg)
   由图可知，婴幼儿为女孩的销售量较女孩更大一些，而未出生购买商品的用户占比很小，所以应该加大用户家婴幼儿是女孩的推广力度以及产品制造。  
   
4. 不同性别购买商品种类的关系
   ``` python
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
   
   ```

    ![不同性别购买商品种类的关系](https://raw.githubusercontent.com/YukaKazemi/taobao-mum-baby/131e6a329b1a47ccc0f401d9a467d525c5f26ab6/tmp/%E4%B8%8D%E5%90%8C%E6%80%A7%E5%88%AB%E8%B4%AD%E4%B9%B0%E5%95%86%E5%93%81%E7%A7%8D%E7%B1%BB%E7%9A%84%E5%85%B3%E7%B3%BB.svg)
   由图可知，已出生婴幼儿对编号50008168商品需求量较大，婴幼儿女孩对编号50014815需求量高于男孩，，而未出生购买50014815最高其他商品需求偏低，应对此现状提高或减少生产量   或者加大宣传力度。  
   
6. 销量与月份关系
   ``` python
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
   ```
   ![销量与月份关系](https://raw.githubusercontent.com/YukaKazemi/taobao-mum-baby/9935f92e2c072380da95c3d2e4a1ffe64e28bb96/tmp/%E9%94%80%E9%87%8F%E4%B8%8E%E6%9C%88%E4%BB%BD%E8%B5%B0%E5%8A%BF%E5%9B%BE.svg)

   分析波峰：在每年的10到11月份左右会有一个大波峰，每年的5月以及9月左右会有一个小波峰，在这段时间销量较同期会有一个明显的涨幅
   推测1：节日因素，在5月有劳动节，母亲节；9月有中秋节；而是10月到11月左右有国庆节、万圣节、立冬、感恩节等节日，平台在这些节日可能绘有促销打折，这时随着价格降低需求量 
   会增加，同时销售量也会增加。
   推测2：双十一打折力度高，淘宝双十一是从2009年开始便存在的大型购物促销狂欢日，而又伴随着即将到来的春节假期，顾客可能进行囤货，结合两个因素导致需求量大幅上升，所以在
   11月前会出现一个大型的销量波峰。  
   结论：在5月与9月以及11月需要加大供货量，保证供需平衡。

   分析波谷：每年的1月左右会出现一个明显的销量波谷，说明这段时间的销量较同期低。
   推测：1月份正值春节，店铺休息，而开着的店铺肯定会抬高物价，而用户在11月进行囤货所以导致1月份的需求量减小，出现销量波谷。
   结论：1月销量惨淡，需要考虑减少进货量的问题，适当降低物价拓宽销售渠道加大宣传力度。
   
