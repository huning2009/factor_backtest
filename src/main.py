#coding:utf-8
#author:zhuhelin,daitangyu,guandong,liuhongjie,lubohua
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from commonUtils import readFile
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
path = "../RawData/AShareEODPrices after 20100101.csv"
#path = "../RawData/test1.csv"


#读取文件
data = readFile(path)

#pivot成dataframe
data = data.pivot(index = 'S_INFO_WINDCODE', columns = 'trade_dt')

#取出数据
open = data['S_DQ_OPEN']
preclose = data['S_DQ_PRECLOSE']
close = data['s_dq_close']
avgPrice = data['S_DQ_AVGPRICE']
tradestatus = data['S_DQ_TRADESTATUS'].shift(-1,axis=1)

#处理异常情况
islimit = (close/preclose-1)*10>0.95
todyyield = avgPrice.shift(-2,axis=1)/avgPrice.shift(-1,axis=1)-1
factor = open/preclose-1
factor[tradestatus=='停牌'] = np.nan
factor[islimit==1]  = np.nan

#分组排序计算收益率
rank = (factor.rank(axis=0,pct=True,method = 'dense',na_option = 'keep')*10 ).apply(np.ceil)
df = pd.merge(np.mean(todyyield[rank==1][todyyield[rank==1]!=0]).to_frame(),np.mean(todyyield[rank==2][todyyield[rank==2]!=0]).to_frame(),how='outer',on='trade_dt')

for i in range(3,11):
    df = pd.merge(df,np.mean(todyyield[rank==i][todyyield[rank==i]!=0]).to_frame(),how='outer',on='trade_dt')

#重命名列
df.columns = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10']
#对冲均值
df1 = df.sub(df.mean(axis=1),axis=0)
#收益累加
dfcumsum = df1.cumsum()
dfcumsum.plot()
dfcumsum.to_csv('../output/result.csv')

