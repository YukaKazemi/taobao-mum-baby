# 淘宝母婴购物数据可视化分析
## 数据集概述
数据集是阿里云天池的数据集:淘宝母婴购物数据的两个csv文件。  
[tianchi_mum_baby.csv](https://github.com/YukaKazemi/taobao-mum-baby/blob/master/data/tianchi_mum_baby.csv)  
[tianchi_mum_baby_trade_history.csv](https://github.com/YukaKazemi/taobao-mum-baby/blob/master/data/tianchi_mum_baby_trade_history.csv)  
包含了953个孩子的的生日和性别数据和29971条淘宝用户的历史交易数据。   
1.tianchi_mum_baby.csv  

| 列 | 描述 |
| ------ | ------ |  
| user_id | 用户 ID (Bigint). |  
| birthday | Children’s birthday (e.g. 20130423). |  
| gender | Children’s gender (“0” 女, “1” 男, “2” 未知). |

2.tianchi_mum_baby_trade_history.csv

| 列 | 描述 |
| ------ | ------ |  
|  | ID (Bigint). |  
| user_id | 用户ID (Bigint). |  
| auction_id | 购买行为编号ID (Bigint). |
| category_2 | Category ID (Bigint). 类别ID |
| category_1 | Root category ID (Bigint). 根类别ID |
| buy_mount | Purchase quantity (Bigint). 采购量 |
| day | Timestamp. |
