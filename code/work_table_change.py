# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 12:33:42 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import re
from openpyxl import load_workbook

def get_not_nan(s1,column):
    try:
       r=s1[column]
       if np.isnan(r):
          number=''
       else:
           if column=='能耗/门槛':
               number=str(1-r)
           else:
               number=str(r)    
    except Exception as e:
        number=''
        print(column,r)
    return number

def get_detail(df):
    list0=[]
    for x in df.index:
        s=df.loc[x]
        s1,s2=s['最大电机总功率_X'],s['动力蓄电池组总能量(kWh)_M_Max']
        if (np.isnan(s1))&(np.isnan(s2)):
                    mot_bat=''
        else:
                    mot_bat=str(s1/s2)
        detail=('参数信息\n'+'  整备质量:'+ get_not_nan(s,'整备质量(kg)_X_Max')+'\n'+
             '  电池能量密度:'+ get_not_nan(s,'电池系统能量密度(Wh/kg)_X_Max')+'\n'+
             '  电耗优于门槛值:'+ get_not_nan(s,'能耗/门槛')+'\n'+
             '  续航里程：'+ get_not_nan(s,'续驶里程(km，工况法)_X_Max')+'\n'+
             '  电机总功率/电池容量：'+ mot_bat)
        list0.append(detail)
    return '\n'.join(list0)

def get_not_nan_name(df,column):
    df=df[df[column].notna()]
    if df.empty:
        s=''
    else:
        s=df.iloc[0][column] 
    return s

def get_one_row(name0,name1,model,df):
    list0=[name0,name1,get_not_nan_name(df,'通用名称_M')]
    for date in ['2017Q1','2017Q2','2017Q3','2017Q4','2018Q1','2018Q2','2018Q3']:
        list0.append(get_detail(df[df['date']==date]))
    return list0
        

def get_rows(name0,name1,df):
    lists=[]
    models=list(set(df[df['model'].notna()]['model'].values))
    for model in models:
        lists.append(get_one_row(name0,name1,model,df[df['model']==model]))
    return lists
        
def get_rowss(name,df):
    list0=[]
    df=df[df['class']==name]
    models=list(set(df[df['model'].notna()]['model'].values))
    name1s=list(set(df[df['整车厂企业简称_X'].notna()]['整车厂企业简称_X'].values))
    for name1 in name1s:
        list0=list0+get_rows(name,name1,df[df['整车厂企业简称_X']==name1])
    return list0
    

def create_table(names,df):
    content=[]
    columns=['车型级别','统计类别','能量密度1.1','能量密度1.2',
             '能效1.1','总系数1.21','总系数1.32']
    for name in names:
        rows=get_rows(name,df)
        content=content+rows
        
    df1=pd.DataFrame(content,columns=columns)
    return  df1
    
def get_unify(name,list0):
    if name in list0:
        name= list0[0]
    return name   

def get_car_class(s):
      if np.isnan(s):
          detail=''
      elif  s<4000:
          detail='A00'
      elif  s>=4000 and s<4400:
          detail='A0'
      elif s>=4400 and s<4600:
          detail='A'
      elif s>=4600 and s<4800:
          detail='A+'
      elif s>=4800:
          detail='B级及以上'
      return detail
  
def get_power(s):
    if np.isnan(s):
          p=''
    elif int(s)==s:
        p=str(int(s))
    elif int(s)!=s:
        p=str(s)
    return p

def get_car_eden(s):
      if np.isnan(s):
          w=''
      elif  s>=140:
          w='能量密度1.1'
      else:
          w=''       
      return w
def get_car_eden1(s):
      if np.isnan(s):
          w=''
      elif  s>=160:
          w='能量密度1.2'
      else:
          w=''       
      return w
  
def get_car_eff(s):
      if np.isnan(s):
          w=''
      elif  s<=0.75:
          w='能效1.1'
      else:
          w=''       
      return w
def get_car_allk1(s):
      if np.isnan(s[0])&np.isnan(s[1]):
          w=''
      elif  (s[1]<=0.75)&(s[0]>=140):
          w='总系数1.21'
      else:
          w=''       
      return w
def get_car_allk2(s):
      if np.isnan(s[0])&np.isnan(s[1]):
          w=''
      elif  (s[1]<=0.75)&(s[0]>=160):
          w='总系数1.32'
      else:
          w=''       
      return w
    
def modify_model(df):
    df['model']=''
    longs=df[df['外廓尺寸长(mm)_X_Max'].notna()].groupby('外廓尺寸长(mm)_X_Max').count().index
    for long in longs:
        df1=df[df['外廓尺寸长(mm)_X_Max']==long]
        for x in  df1.index:
            s=df1.loc[x,'产品型号_X']
            p=df1.loc[x,'最大电机总功率_X']
            number=re.findall(r'(\d+?\d*)', s)[0]
            com=re.findall(r'([A-Za-z]+?[A-Za-z]*)', s)[0]
            com=get_unify(com,['JL','HQ','MR','SMA'])
            com=get_unify(com,['HMA','HMC'])
            df.loc[x,'model']=com+'_'+number[:2]+'_'+str(int(long))+ '_'+get_power(p)
    list0,list1,list2,list3,list4,list5,list6=[],[],[],[],[],[],[]
    for i in range(0,len(df)):
           list0.append(get_car_class(df.loc[i,'外廓尺寸长(mm)_X_Max']))
    df['class']=list0
    for i in range(0,len(df)):
           list1.append(get_car_eden(df.loc[i,'电池系统能量密度(Wh/kg)_X_Max']))
    df['能量密度1.1']=list1
    for i in range(0,len(df)):
           list2.append(get_car_eden1(df.loc[i,'电池系统能量密度(Wh/kg)_X_Max']))
    df['能量密度1.1']=list2
    for i in range(0,len(df)):
           list3.append(get_car_eff(df.loc[i,'能耗/门槛']))
    df['能效1.1']=list3
    for i in range(0,len(df)):
           list4.append(get_car_allk1(df.loc[i,['电池系统能量密度(Wh/kg)_X_Max','能耗/门槛']]))
    df['总系数1.21']=list4
    for i in range(0,len(df)):
           list5.append(get_car_allk2(df.loc[i,['电池系统能量密度(Wh/kg)_X_Max','能耗/门槛']]))
    df['总系数1.32']=list5
    
    
    return df   
       
        
   

def main():
    
    df=pd.read_csv('table_merge.csv')
    df=modify_model(df)
    names=['A00','A0','A','A+','B级及以上']
    df1=create_table(names,df)
    book = load_workbook('table.xlsx')
    writer = pd.ExcelWriter('table.xlsx', engine = 'openpyxl')
    writer.book = book
    #df1.set_index('级别').to_csv('table5.csv')
    df1.set_index('级别').to_excel(writer,'Sheet5')
    writer.save()
    writer.close()
    
if __name__=='__main__':
    main()
