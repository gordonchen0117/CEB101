import re
import json
import pymongo
from pymongo import MongoClient
import pprint
import jieba

client = MongoClient('localhost', 27017)
db = client['ceb101']
col = db['Ming_zone1']

jieba.load_userdict('./company.txt')

find_list = list()
for i in col.find({},{"title":1,"_id":0}):
    find_list.append(i)
    
n = 0
m = 0
def run() :
    re_words_Established =re.findall("主文.*", rep)[0].replace('主文','|').replace('。','|').split('|')[1] \
                                .replace('不受理','不成立')
    try :
        re_word_rule = re.findall("商標法施行細則.{0,20}", rep)[0].replace("第",' ').replace('類',' ').split(' ')[2]
    except :
        re_word_rule ='None'


    law_re = re.findall("商標法第.{0,3}", rep)
    law_res = list()
    for i in law_re :
        try :
            res = int(i.replace('條','').split('第')[1])

            law_res.append(res)
        except :
            pass

    re_res = re.findall("爰依.{0,20}", rep)
    try :
        add_re_res = re_res[0].replace("第"," ").replace("條"," ").split(" ")
        for j in add_re_res :
            try :
                law_res.append(int(j))
            except :
                pass
    except :
        pass
    law_list = list()
#     print(law_res)
    for x in law_res:
        if x not in law_list:
            law_list.append(x)
#     law_str ="、".join(law_list)


    key_word1 = len(re.findall("有可能.{0,40}誤認", rep))
    key_word2 = len(re.findall("爰依.", rep))
    key_word3 = len(re.findall("屬構成近似之商標.", rep))
    key_word4 = len(re.findall("不具.{0,20}識別", rep))
    key_word5 = len(re.findall("應予撤銷.", rep))
    key_word6 = len(re.findall("系爭.{0,20}撤銷", rep))
    key_word7 = len(re.findall("有致.{0,40}誤認", rep))
    key_word8 = len(re.findall("不成立.", rep))
    key_word9 = len(re.findall("應具有.{0,20}識別.", rep))
    key_word10 = len(re.findall("近似程度極低.", rep))
    key_word11 = len(re.findall("不會.{0,30}誤認", rep))
    key_word12 = len(re.findall("無法認定.", rep))
    key_word13 = len(re.findall("不會.{0,30}混淆", rep))

    zone1_dict['title'] = zone1['title']
    zone1_dict['plaintiff'] = re_words_plaintiff
    zone1_dict['defendant'] = zone1['markname'].replace('及圖','')
    zone1_dict['rule'] = re_word_rule
    zone1_dict['key_word1'] = key_word1  #有可能...誤認
    zone1_dict['key_word2'] = key_word2 #爰依
    zone1_dict['key_word3'] = key_word3  #屬構成近似之商標
    zone1_dict['key_word4'] = key_word4  #不具...識別
    zone1_dict['key_word5'] = key_word5  #應予撤銷
    zone1_dict['key_word6'] = key_word6  #系爭...撤銷
    zone1_dict['key_word7'] = key_word7  #有致...誤認
    zone1_dict['key_word8'] = key_word8  #不成立
    zone1_dict['key_word9'] = key_word9  #應具有...識別
    zone1_dict['key_word10'] = key_word10 #近似程度極低
    zone1_dict['key_word11'] = key_word11 #不會...誤認
    zone1_dict['key_word12'] = key_word12 #無法認定
    zone1_dict['key_word13'] = key_word13 #不會...混淆
    for i in range(1,112):
        zone1_dict['law_'+str(int(i))] = 0

    for i in law_list :
        if i < 112 :

            zone1_dict['law_'+str(int(i))] += 1

    established = re.findall('異議不成立',re_words_Established)
    if len(established) != 0 :
        zone1_dict['established'] = 0
    else :
        zone1_dict['established'] = 1

        
for zone1_title in find_list :
    zone1_dict = {}
    zone1 = col.find_one(zone1_title)
    rep = zone1['content'].replace('（',' ').replace('）',' ').replace('：','').replace(':','')


    try:
        re_words_plaintiff_jieba =jieba.cut(re.findall("正本 .{0,30}", rep)[0].split(' ')[1].split('【')[0])

        for i in re_words_plaintiff_jieba :
            i_len = len(re.findall("公司", i))
            if i_len != 0 :
                re_words_plaintiff_company = i
        try :
            re_word_rule = re.findall("商標法施行細則.{0,20}", rep)[0].replace("第",' ').replace('類',' ').split(' ')[2]
        except :
            re_word_rule ='None'

        try: 
            col_trade = db['trademark_jsonData']
            re_words_plaintiff_json = col_trade.find_one({"company":re_words_plaintiff_company,"goodsclass-code" : re_word_rule.split('、')[0]})
            re_words_plaintiff = re_words_plaintiff_json['tmark-name']
#                     print(re_words_plaintiff_company)
#                     print(re_words_plaintiff['tmark-name'])
        except :
            continue
    except :
        re_words_plaintiff_jieba =jieba.cut(re.findall("異議人.{0,40}", rep)[0].replace('<','人').split('人')[1])

        for i in re_words_plaintiff_jieba :
            i_len = len(re.findall("公司", i))
            if i_len != 0 :
                re_words_plaintiff_company = i
        try :
            re_word_rule = re.findall("商標法施行細則.{0,20}", rep)[0].replace("第",' ').replace('類',' ').split(' ')[2]
        except :
            re_word_rule ='None'

        try :
            col_trade = db['trademark_jsonData']
            re_words_plaintiff_json = col_trade.find_one({"company":re_words_plaintiff_company,"goodsclass-code" : re_word_rule.split('、')[0]})
            re_words_plaintiff = re_words_plaintiff_json['tmark-name']
        except :
            continue
            
            
    re_similar_word = re.findall(".{0,10}圖樣.{0,20}",rep)
#     re_similar_word_1 = re.findall(".{0,10}文.{0,20}區辨",rep)
    if len(re_similar_word) != 0 :
        run()
        n += 1   
        photo_dict = dict()
        col_final_data_zone1_zone2 = db['final_data_zone1_zone2']
        re_photo_id_json = col_final_data_zone1_zone2.find_one(zone1_title)
        photo_dict["title"] = re_photo_id_json["title"]
        photo_dict["tmark_id"] = re_photo_id_json["tmark_id"]
        photo_dict["established"] = re_photo_id_json["established"]
        print(photo_dict)
#         print(zone1['title'])
    #     zone1_dict['established'] = re_words_Established
    #     print(zone1_dict)
    #     print("title:",zone1['title'])
    #     print(re_words_plaintiff)
    #     print("defendant:",zone1['markname'])
    #     print(re_words_Established)
    #     print(re_word_rule) 
        print(n)
#         print(m)
        print("-"*20)
        with open('final_data_similar_photo.json','a',encoding = 'utf-8') as f :
            json.dump(photo_dict, f, ensure_ascii=False)
