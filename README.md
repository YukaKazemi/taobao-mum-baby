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
##数据预处理
以时间段较长的奶粉为例.  
对配方奶粉的分段，主要是根据国际食品法典委员会制定的cac来进行划分。  
婴幼儿奶粉现在大范围上基本分为一段、二段、三段，部分婴幼儿奶粉可能会分为四段、五段。  
奶粉分段及适用年龄：  
第1段婴幼儿奶粉适合0~6个月的宝宝；  
第2段婴幼儿奶粉适合6~12个月的宝宝；  
第3段婴幼儿奶粉适合1周岁~3周岁的宝宝；  
第4段奶粉适合3周岁~7周岁的孩子。  
7周岁最多为365*7=2555天，那么对于天数大于2560天的天数视为无效数据，删除行  

