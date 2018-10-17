# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 09:34:21 2018

@author: Administrator
"""

import pandas as pd
import re


df=pd.read_csv('table_evpromot_announce_taxfree_merge_change_cal_slim_ev.csv')

def get_unify(name,list0):
    if name in list0:
        name= list0[0]
    return name

def record_unify_fail(df):
    df=df[df['整车厂企业简称_X']=='']
    df[['企业_X']].to_csv('table_evpromot_unify_fail.csv')


def get_company_name_unify(string):
    list=['江铃','东风','华晨鑫源','东风雷诺','长江乘用车','御捷车业','云度新能源','豪情汽车','一汽海马','通家汽车',
          '江南汽车','长安','江淮','力帆','比亚迪','知豆','广州汽车','金龙客车','奇瑞','北汽福田',
          '北京汽车','北京新能源','上汽大通','上汽通用五菱','东南','日产','长城','上海汽车','一汽夏利','广汽丰田',
          '海马','金华青年','北京现代','野马汽车','一汽吉林','九龙','吉利','潍柴','猎豹','华晨','宝沃','成功',
          '北汽新能源','黄海','昌河','北汽银翔','荣成华泰','北汽','卡威','昌河铃木','中国第一汽车','汉腾','中兴',
          '凯翼','上汽大众','广汽本田','红星','飞碟','上汽通用','广汽吉奥','新龙马','广汽吉奥','一汽丰田','一汽-大众',
          '上海大众','哈飞','华普','上海通用','前途','广汽三菱','威马','合众','安达尔','一汽客车','广通','宇通','中博',
          '亚星','华奥','中车时代','沂星','中汽宏远','源正','陆地方舟','金龙联合','申龙客车','五洲龙','南京汽车','安凯',
          '博能上饶客车','万象','金龙旅行车','国宏','山西新能源','广通','北方华德尼奥普兰客车','亚星','扬子江汽车','大运',
          '四川省客车','北奔重型','舒驰','中通','五龙','中植一客','华策','长江','万向','大汉','南京市公共交通车辆厂','天洋',
          '镇江汽车','豪沃','重汽','武汉客车','新福达','宜春','中航爱维客','成都客车','梅花','新筑通工','通联','中车电车',
          '少林','皇城相府宇航','常隆','飞驰','贵航云马','航天神州','恒通','星凯龙','乾丰','华龙','牡丹','西虎','申沃',
          '恩驰','跃迪','新楚风','陕西汽车','九州','之信','上汽唐山客车','登达','南车电车','友谊','安源','龙华','秦星',
          '北车','凯马百路佳','穗通','桂林客车','吉姆西','原野','冀东华夏','京华','越西','云山','中威','现代','四川汽车',
          '南车时代','中骐','齐鲁','益茂','顺达','紫金江发','神马','宝龙集团湛江万里','中植','昆明客车','陕西汉中','中车',
          '中集凌宇','中上','森源艾思特福','衡山','龙江','沃尔沃','克莱斯勒']
    company_name_unify=''
    for x in list:
        if x in string:
            company_name_unify=x
            break
    company_name_unify=get_unify(company_name_unify,['上汽大众','上海大众'])
    company_name_unify = get_unify(company_name_unify, ['上汽通用', '上海通用'])
    company_name_unify = get_unify(company_name_unify, ['北京汽车', '北汽','北京新能源','北汽新能源','北汽银翔'])
    company_name_unify = get_unify(company_name_unify, ['吉利', '豪情汽车'])
    company_name_unify = get_unify(company_name_unify, ['一汽', '中国第一汽车','一汽吉林'])
    company_name_unify = get_unify(company_name_unify, ['海马', '一汽海马'])
    return company_name_unify

def get_data_max(data,column):
  for x in column:
     content = []
     for i in range(0, len(data)):
        if data.loc[i,x] == '' :
            content.append('')
        else:
             value=re.findall(r'\d+\.?\d*',data.loc[i,x])
             if len(value)==0:
                 content.append('')
             else:
                content.append(max([float(y) for y in value]))
     data[x+'_Max']=content
  return data

def main():
    df=pd.read_csv('table_evpromot_announce_taxfree_merge_change_cal_slim_phev.csv').astype(str)
    df = df.replace(to_replace=re.compile(r'.*nan.*'), value='')
    names=[]
    column_max=['动力蓄电池组总能量(kWh)_M']
    df=get_data_max(df, column_max)
    for i in range(0,len(df)):
        names.append(get_company_name_unify(df.loc[i,'企业_X']))
    df['整车厂企业简称_X']=names
    df.set_index('企业_X').to_csv('table_merge1.csv')
    record_unify_fail(df)

if __name__=='__main__':
     main()
     



