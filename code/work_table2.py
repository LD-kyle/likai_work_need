# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:55:42 2018

@author: Administrator
"""
import pandas as pd
import re
from openpyxl import load_workbook


def get_not_nan(df,column):
    df=df[df[column].notna()]
    if df.empty:
        number=''
    else:
        if column=='能耗/门槛':
            number=str(1-df.iloc[0][column])
        else:
            number=str(df.iloc[0][column])    
    return number


def get_detail(df):
    models=df[df['model'].notna()].groupby('model').count().index
    b,list0=0,[]
    for model in models:
        df2=df[df['model']==model]
        df3=df2.groupby('最大电机总功率_X').count()
        b=b+len(df3)
        for power in df3.index:
                #df4=df2[(df2['最大电机总功率_X']==power)&(df2['通用名称_M'].notna())]
                df4=df2[df2['最大电机总功率_X']==power]
                df5=df4[(df4['最大电机总功率_X'].notna())&(df4['动力蓄电池组总能量(kWh)_M_Max'].notna())]
                if df5.empty:
                    mot_bat=''
                else:
                    mot_bat=str(df5.iloc[0]['最大电机总功率_X']/df5.iloc[0]['动力蓄电池组总能量(kWh)_M_Max'])
                detail=('1.车型名称:'+get_not_nan(df4,'通用名称_M')+'\n'+
                        '2.参数信息\n'+'  整备质量:'+ get_not_nan(df4,'整备质量(kg)_X_Max')+'\n'+
                        '  电池能量密度:'+ get_not_nan(df4,'电池系统能量密度(Wh/kg)_X_Max')+'\n'+
                        '  电耗优于门槛值:'+ get_not_nan(df4,'能耗/门槛')+'\n'+
                        '  续航里程：'+ get_not_nan(df4,'续驶里程(km，工况法)_X_Max')+'\n'+
                        '  电机总功率/电池容量：'+ mot_bat)
                list0.append(detail)
    return b,'\n'.join(list0)

def get_count_number(df):
    car_l=df['外廓尺寸长(mm)_X_Max']
    sum0,sum0_1=get_detail(df[car_l.notna()])
    A00,A00_1=get_detail(df[car_l<4000])
    A0,A0_1=get_detail(df[(car_l>=4000)&(car_l<4400)])
    A,A_1=get_detail(df[(car_l>=4400)&(car_l<4600)])
    A_add,A_add_1=get_detail(df[(car_l>=4600)&(car_l<4800)])
    B,B_1=get_detail(df[car_l>=4800])
    df1=df[df['电池系统能量密度(Wh/kg)_X_Max'].notna()]
    df2=df[df['能耗/门槛'].notna()]
    if df1.empty:
        bat_en_den=''
    else:
        bat_en_den=max(df1['电池系统能量密度(Wh/kg)_X_Max'].values)
    if df2.empty:
        eff=''
    else:
        eff=1-min(df2['能耗/门槛'].values)  
    return [A00,A0,A,A_add,B,sum0,bat_en_den,eff],[A00_1,A0_1,A_1,A_add_1,B_1,bat_en_den,eff]


def get_unify(name,list0):
    if name in list0:
        name= list0[0]
    return name   
    
def modify_model(df):
    df['model']=''
    longs=df[df['外廓尺寸长(mm)_X_Max'].notna()].groupby('外廓尺寸长(mm)_X_Max').count().index
    for long in longs:
        df1=df[df['外廓尺寸长(mm)_X_Max']==long]
        for x in  df1.index:
            s=df1.loc[x,'产品型号_X']
            number=re.findall(r'(\d+?\d*)', s)[0]
            com=re.findall(r'([A-Za-z]+?[A-Za-z]*)', s)[0]
            com=get_unify(com,['JL','HQ','MR','SMA'])
            com=get_unify(com,['HMA','HMC'])
            df.loc[x,'model']=com+'_'+number[:2]+'_'+str(int(long))           
    #for i in range(0,len(df)):
        #s=df.loc[i,['产品型号_X','外廓尺寸长(mm)_X_Max']]
        #list0.append(re.search(r'^(.*[^\d]+)\d*$', s).group(1))
        
    #df['model']=list0
    return df   
    

def get_row(name,df):
    df1=df[df['整车厂企业简称_X']==name]
    wh,e_limit=df1['电池系统能量密度(Wh/kg)_X_Max'],df1['能耗/门槛']  
    rows=get_count_number(df1[(wh>=140)&(e_limit<=0.75)])
    return [name]+rows[0],[name]+rows[1]


def create_table(names,df):
    columns=['企业名称','A00级“双达标”车型数','A0级“双达标”车型数',
             'A级“双达标”车型数	','A+级“双达标”车型数','B级及以上“双达标”车型数',
             '合计“双达标”车型数','最高电池能量密度（Wh/kg）','能耗优于门槛值(%)']
    columns1=['企业名称','A00级“双达标”车型数','A0级“双达标”车型数',
             'A级“双达标”车型数	','A+级“双达标”车型数','B级及以上“双达标”车型数',
             '最高电池能量密度（Wh/kg）','能耗优于门槛值(%)']
    content,content1=[],[]
    for name in names:
        rows=get_row(name,df)
        content.append(rows[0])
        content1.append(rows[1])
        
    df1=pd.DataFrame(content,columns=columns)
    df2=pd.DataFrame(content1,columns=columns1)
    return  df1,df2
    
        
        
        

def main():
    
    df=pd.read_csv('table_merge.csv')
    names=list(set(df[df['整车厂企业简称_X'].notna()]['整车厂企业简称_X'].values))
    df=modify_model(df)
    df1,df2=create_table(names,df)
    #df1.set_index('企业名称').to_csv('table3.csv')
    #df2.set_index('企业名称').to_csv('table4.csv')
    book = load_workbook('table.xlsx')
    writer = pd.ExcelWriter('table.xlsx', engine = 'openpyxl')
    writer.book = book
    df1.set_index('企业名称').to_excel(writer,'Sheet3')
    df2.set_index('企业名称').to_excel(writer,'Sheet4')
    writer.save()
    writer.close()
   
    
if __name__=='__main__':
    main()
    
        
