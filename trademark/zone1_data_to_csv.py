import re
import json
import pymongo
from pymongo import MongoClient
import pprint
import csv
import pandas as pd

client = MongoClient('localhost', 27017)
db = client['ceb101']
col = db['final_data_photo_similar']

find_list = list()
for i in col.find({},{"title":1,"_id":0}):
    if i != None :
        find_list.append(i)
# find_list

zone1_dict = {}
for zone1_title in find_list :
    zone1 = col.find_one(zone1_title)
#     print(zone1)
    try :
        zone1_dict[zone1['title']] = [zone1['tmark_id'],zone1['established']]
    except :
        pass
        
# print(zone1_dict)
columns = ['tmark_id','established']
zone1_pd = pd.DataFrame.from_dict(data = zone1_dict, orient='index',columns = columns)
# print(zone1_pd)
zone1_csv = zone1_pd.to_csv('final_data_photo_similar_test.csv', encoding = 'utf-8')

zone1_pd
