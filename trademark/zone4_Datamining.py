import re
import json
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['ceb101']
col = db['Ming_zone4']

find_list = list()
for i in col.find({},{"title":1,"_id":0}):
    find_list.append(i)
# find_list

n = 0
for zone4_title in find_list :
    zone4_dict = {}
    zone4 = col.find_one(zone4_title)
    rep = zone4['content'].replace('（',' ').replace('）',' ')
    try:
        re_words_class =re.findall("第19條.{0,20}", rep)[0]
        try :
            re_words_plaintiff = re.findall("註冊.{0,20}「.{0,50}」商標", rep)[0].replace('「','|').replace('」','|').split('|')[1]
        except IndexError:
            try :
                re_words_plaintiff = re.findall("核駁著名.{0,10}「.{0,50}」商標", rep)[0].replace('「','|').replace('」','|').split('|')[1] 
            except IndexError:
                try :
                    re_words_plaintiff = re.findall("據以核駁.{0,20}「.{0,50}」商標", rep)[0].replace('「','|').replace('」','|').split('|')[1] 
                except IndexError:
                    try :
                        re_words_plaintiff = re.findall("據駁.{0,20}「.{0,50}」商標", rep)[0].replace('「','|').replace('」','|').split('|')[1] 
                        
                    except :
#                         print(zone4['title'])
                        continue
        re_photo = re.findall("相同.{0,5}文",rep)

        if len(re_photo) != 0 :
            try:

                col_trade = db['trademark_jsonData']
                re_words_plaintiff_json = col_trade.find_one({"tmark-name":re_words_plaintiff})
                re_words_plaintiff_id = re_words_plaintiff_json['_id']

            except :
                continue                

            try :            
                re_words_Established = re.findall("主旨.*?\n", rep)[0].split('\\n')[0].split('，')[1].replace('主旨：','')
            except :
                re_words_Established = "應予核駁"

        #     re_words_Established =re.findall("主文.*", rep)[0].replace('主文','|').replace('。','|').split('|')[1] \
        #                                 .replace('不受理','不成立')
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
        # #     law_str ="、".join(law_list)


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

            zone4_dict['title'] = zone4['title']
            zone4_dict['plaintiff'] = re_words_plaintiff
            zone4_dict['defendant'] = zone4['markname'].replace('及圖','')
        #     zone4_dict['law'] = law_list
            zone4_dict['rule'] = re_word_rule
            zone4_dict['key_word1'] = key_word1  #有可能...誤認
            zone4_dict['key_word2'] = key_word2 #爰依
            zone4_dict['key_word3'] = key_word3  #屬構成近似之商標
            zone4_dict['key_word4'] = key_word4  #不具...識別
            zone4_dict['key_word5'] = key_word5  #應予撤銷
            zone4_dict['key_word6'] = key_word6  #系爭...撤銷
            zone4_dict['key_word7'] = key_word7  #有致...誤認
            zone4_dict['key_word8'] = key_word8  #不成立
            zone4_dict['key_word9'] = key_word9  #應具有...識別
            zone4_dict['key_word10'] = key_word10 #近似程度極低
            zone4_dict['key_word11'] = key_word11 #不會...誤認
            zone4_dict['key_word12'] = key_word12 #無法認定
            zone4_dict['key_word13'] = key_word13 #不會...混淆
            for i in range(1,112):
                zone4_dict['law_'+str(int(i))] = 0

            for i in law_list :
                if i < 112 :

                    zone4_dict['law_'+str(int(i))] += 1

            established = re.findall('不成立',re_words_Established)
            if len(established) != 0 :
                zone4_dict['established'] = 0
            else :
                zone4_dict['established'] = 1
            n +=1

#         print(zone4['title'])
#         print(zone4['markname'])
#         print(re_words_plaintiff)
#         print(law_list)
    #     zone4_dict['established'] = re_words_Established
#         print(zone4_dict)
    #     print("title:",zone4['title'])
        
    #     print("defendant:",zone4['markname'])
#     print(re_words_Established)
#         print(re_word_rule) 
#         print("-"*20)
            print(n)
        with open('zone4_data_similar_word.json','a',encoding = 'utf-8') as f :
            json.dump(zone4_dict, f, ensure_ascii=False)
        
#         print(m)
    except :
        pass
  
