# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 09:50:16 2018

@author: Administrator
"""

import pandas as pd 
import re



def count_number(df):
    df1=df[df['整车厂企业简称_X'].notna()].groupby('整车厂企业简称_X').count()
    a=len(df1)
    a1='\n'.join(list(df1.index))
    models=df[df['model'].notna()].groupby('model').count().index
    b,list0=0,[]
    for model in models:
        df2=df[df['model']==model]
        df3=df2.groupby('最大电机总功率_X').count()
        b=b+len(df3)
        for power in df3.index:
            df4=df2[(df2['最大电机总功率_X']==power)&(df2['通用名称_M'].notna())]
            if df4.empty:
                list0.append('')
            else:
                list0.append(df4.iloc[0]['通用名称_M']+':'+str(power))
                  
            
    return a,b,a1,'\n'.join(list0)

def get_lines(df,name):
    wh,e_limit=df['电池系统能量密度(Wh/kg)_X_Max'],df['能耗/门槛']
    den11_0,den11_1,den11_2,den11_3=count_number(df[wh>=140])
    den12_0,den12_1,den12_2,den12_3=count_number(df[wh>=160])
    eff0,eff1,eff2,eff3=count_number(df[e_limit<=0.75])
    sum121_0,sum121_1,sum121_2,sum121_3=count_number(df[(wh>=140)&(e_limit<=0.75)])
    sum132_0,sum132_1,sum132_2,sum132_3=count_number(df[(wh>=160)&(e_limit<=0.75)])
    list0=[name,'企业数量',den11_0,den12_0,eff0,sum121_0,sum132_0]
    list1=[name,'车型数量',den11_1,den12_1,eff1,sum121_1,sum132_1]
    list2=[name,'包含企业',den11_2,den12_2,eff2,sum121_2,sum132_2]
    list3=[name,'包含车型',den11_3,den12_3,eff3,sum121_3,sum132_3]
    return [list0,list1],[list2,list3]

def create_number_table(df):
    columns=['车型级别','统计类别','能量密度1.1','能量密度1.2',
             '能效1.1','总系数1.21','总系数1.32']
    df=df[['整车厂企业简称_X','能耗/门槛',
           '电池系统能量密度(Wh/kg)_X_Max','最大电机总功率_X',
           '企业_X','外廓尺寸长(mm)_X_Max','model','通用名称_M']]
    car_l=df['外廓尺寸长(mm)_X_Max']
    A00,A00_n=get_lines(df[(car_l<4000)&(car_l.notna())],'A00')
    A0,A0_n=get_lines(df[(car_l>=4000)&(car_l<4400)&(car_l.notna())],'A0')
    A,A_n=get_lines(df[(car_l>=4400)&(car_l<4600)&(car_l.notna())],'A')
    A_add,A_add_n=get_lines(df[(car_l>=4600)&(car_l<4800)&(car_l.notna())],'A+')
    B,B_n=get_lines(df[(car_l>=4800)&(car_l.notna())],'B级及以上')
    com,com_n=get_lines(df[(car_l.notna())],'合计')
    df1=pd.DataFrame(A00+A0+A+A_add+B+com,columns=columns)
    df2=pd.DataFrame(A00_n+A0_n+A_n+A_add_n+B_n+com_n,columns=columns)

    return  df1,df2 

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

def main():
   df=pd.read_csv('table_merge.csv')
   #df=df.replace(to_replace=re.compile(r'.*nan.*'), value='')
   df=modify_model(df)
   df1,df2=create_number_table(df)
   writer = pd.ExcelWriter('table.xlsx')
   df1.set_index(['车型级别','统计类别']).to_excel(writer,'Sheet1')
   df2.set_index(['车型级别','统计类别']).to_excel(writer,'Sheet2')
   #df1.set_index(['车型级别','统计类别']).to_csv('table1.csv')
   #df2.set_index(['车型级别','统计类别']).to_csv('table2.csv')
   writer.save()
   writer.close()
if __name__=='__main__':
    main()



