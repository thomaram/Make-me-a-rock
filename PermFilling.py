#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:28:58 2019

@author: thomaram
"""

import pandas as pd

path = "~/Hackathon2019/Make-me-a-rock/Data/"

# %notebook inline

data_raw = pd.read_csv(path+"data_1.csv", delimiter=",", encoding = 'cp865')

npd_litho = pd.read_csv(path+"npd_litho_strat.csv", delimiter=";",encoding = 'cp865')

xyz = pd.read_csv(path+"xyz_combined.csv", delimiter=";",encoding ='cp865')

 

data_1 = data_raw[['wellbore','md','kh_kl','kv_kl','well_id','phi_best','clean_litho','grain_density','grain_size','sorting','cement']]

after_grouping = data_1.copy()

after_grouping = after_grouping.iloc[0:0]

data_1['kh_kl']=pd.to_numeric(data_1['kh_kl'], downcast='float', errors='coerce')

groups = data_1.groupby(by='wellbore', sort=False)

for name, group in groups:

    average_kh = group.loc[group['kh_kl'].isnull()==False,'kh_kl'].mean()

    group.loc[group['kh_kl'].isnull()==True,'kh_kl'] = average_kh

    after_grouping = pd.concat([after_grouping, group])

   

data_clean = after_grouping.loc[data_1['wellbore'].isnull()==False]

# first_batch = data_clean.copy()

first_batch = data_clean.loc[ (data_clean['kh_kl'].isnull()==False) & (data_clean['phi_best'].isnull()==False)]

 

first_batch['well_id']=pd.to_numeric(first_batch['well_id'], downcast='integer', errors = 'coerce')

tmp = pd.merge(first_batch, npd_litho, how='inner', left_on='well_id', right_on='npd_id')

# tmp.loc(tmp['md']=='339..90','md')=3399

tmp['md']=pd.to_numeric(tmp['md'], downcast='float',errors = 'coerce')

tmp['md_top']=pd.to_numeric(tmp['md_top'], downcast='float',errors = 'coerce')

tmp['md_bottom']=pd.to_numeric(tmp['md_bottom'], downcast='float',errors = 'coerce')

result = tmp.loc[(tmp['md']>=tmp['md_top'] ) & (tmp['md']<tmp['md_bottom'])]

result = result.drop(columns = ['wellbore_x', 'md_top','md_bottom','npd_id'])

result2 = pd.merge(result, xyz, how='inner', left_on='well_id', right_on='npd_id')

result2['phi_best']=pd.to_numeric(result2['phi_best'], downcast='float',errors = 'coerce')

result2.loc[result2['cement']=='well ','cement']='well cemented'

result2.loc[result2['clean_litho']=='sandstone','clean_litho']='Sandstone'
result2.loc[result2['clean_litho']=='marl (-y)','clean_litho']='Marlstone'
result2.loc[result2['clean_litho']=='siltstone','clean_litho']='Siltstone'
result2.loc[result2['clean_litho']=='Sandstone ','clean_litho']='Sandstone'

result2.to_csv(path+"tmp_batch.csv", encoding = 'cp865')