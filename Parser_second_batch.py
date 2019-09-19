#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:50:36 2019

@author: thomaram
"""

import pandas as pd

path="~/Hackathon2019/Make-me-a-rock/Data/"
data_raw = pd.read_csv(path+"data_1.csv", delimiter=",")

npd_litho = pd.read_csv(path+"npd_litho_strat.csv", delimiter=";",encoding="CP865")

xyz = pd.read_csv(path+"xyz_combined.csv", delimiter=";")

npd_litho = pd.read_csv(path+"npd_litho_strat.csv", delimiter=";", encoding="CP865")

data_1 = data_raw[['wellbore','md','kh_kl','kv_kl','well_id','phi_best','clean_litho','grain_density','grain_size','sorting','cement']]

data_clean = data_1.loc[data_1['wellbore'].isnull()==False]

first_batch = data_clean.dropna(how='any')
first_batch=first_batch.replace(',','.', regex=True)

first_batch['well_id']=pd.to_numeric(first_batch['well_id'], downcast='integer')

tmp = pd.merge(first_batch, npd_litho, how='inner', left_on='well_id', right_on='npd_id')

tmp=tmp.replace('339..90','3399',regex=True)
tmp=tmp.replace('18.69.25','1869.25',regex=True)


tmp['md']=pd.to_numeric(tmp['md'], downcast='float')

tmp['md_top']=pd.to_numeric(tmp['md_top'], downcast='float')

tmp['md_bottom']=pd.to_numeric(tmp['md_bottom'], downcast='float')

result = tmp.loc[(tmp['md']>=tmp['md_top'] ) & (tmp['md']<tmp['md_bottom'])]

result = result.drop(columns = ['wellbore_x', 'md_top','md_bottom','npd_id'])

result2 = pd.merge(result, xyz, how='inner', left_on='well_id', right_on='npd_id')

result2['phi_best']=pd.to_numeric(result2['phi_best'], downcast='float')

 

result2.to_csv(path+"second_batch.csv")