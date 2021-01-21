import re
import json
import pymongo
from pymongo import MongoClient
import jieba

client = MongoClient('localhost', 27017)
db = client['ceb101']
# col = db['final_data_photo']
col = db['final_data_zone1_zone2']

find_list = list()
for i in col.find({},{"_id":1}):
    find_list.append(i)
# find_list

for zone1_title in find_list :
    zone1_dict = {}
    zone1 = col.find_one(zone1_title)
    re_words_plaintiff = zone1['plaintiff']
    col_trade = db['trademark_jsonData']
    re_words_plaintiff_json = col_trade.find_one({"tmark-name":re_words_plaintiff})
    if re_words_plaintiff_json['goodsclass-code'] != 'None' :
        re_words_plaintiff_id =re_words_plaintiff_json['goodsclass-code'] + '_' + re_words_plaintiff_json['_id']
    else :
        re_words_plaintiff_None = 'Empty'
        re_words_plaintiff_id =re_words_plaintiff_None + '_' + re_words_plaintiff_json['_id']

    print(re_words_plaintiff_id)
    col.update(zone1_title,{"$set":{"tmark_id":re_words_plaintiff_id}})
