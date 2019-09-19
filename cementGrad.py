#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:00:54 2019

@author: thomaram
"""
import pandas as pd

path="~/Hackathon2019/Make-me-a-rock/Data/"


second_batch=pd.read_csv(path+"second_batch.csv")
second_batch.insert(11, 'cement_grade', 0, allow_duplicates = False)

#pd.unique(second_batch['cement'])
second_batch=second_batch.replace('well well cemented cemented','well cemented', regex=True)

second_batch=second_batch.replace('well well cemented very well cemented','well cemented very well cemented', regex=True)

second_batch=second_batch.replace('well well cemented fair cemented','well cemented fair cemented', regex=True)

second_batch=second_batch.replace('well ','well cemented', regex=True)

second_batch=second_batch.replace('well cementedcemented','well cemented', regex=True)
second_batch=second_batch.replace('fair cemented well cemented','well cemented fair cemented', regex=True)

second_batch['cement_grade'] = second_batch['cement']



second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('very poorly cemented unconsolidated','14', regex=True)

second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('unconsolidated','15', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('consolidated','1', regex=True)

second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('well cemented very well cemented','3', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('well cemented fair cemented','5', regex=True)

second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('poorly cemented very poorly cemented','11', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('very poorly cemented fair cemented','12', regex=True)

second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('very poorly cemented','13', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('very well cemented','2', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('fair well cemented','7', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('well cemented','4', regex=True)

second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('fair cemented','8', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('poorly cemented','10', regex=True)
second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('cemented','6', regex=True)



#second_batch['cement_grade']=second_batch.loc[:,'cement_grade'].replace('consolidated','1', regex=True)

second_batch.to_csv(path+"second_batch.csv")