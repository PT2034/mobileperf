"""
Created on 2021年10月15日
@author: lz
"""
import csv
import time
import hashlib
import uuid
from datetime import datetime

import requests
import json

from sample.data_processor_utils_v2.CSVUtil import CSVUtil

appKey = "Q93a36gZ"  # test
# appKey = "hZPQU3w9"  # prod
# appSecret = "fc4ec0c2c4dfd2dbabbe42dee4562822"
appSecret = "zuNhL4db4e1kzZJcob7Bj5Kn51T0z3ms"
time_stamp = int(time.time())
# auth = ('ims', 'ims123')
x_xlv_nonce_uuid = str(uuid.uuid4())
x_xlv_nonce = ''.join(x_xlv_nonce_uuid.split('-'))

# test
fetchnlu_url = "http://hmi-in.chengjiukehu.com/monkey-light-demo/fetchnlu"

# prod
# fetchnlu_url = "http://10.171.19.146:8013/fetchnlu" # connection timeout
# fetchnlu_url = "http://t-talk.vdyoo.net/monkey-light-demo/fetchnlu"

class ApplicationAutoDemo():

    def __init__(self):
        print("current fetchnlu_url = ", fetchnlu_url)

    def req_builder(self, asr_info="精神损失", handle_task_type="intent_baike"):
        req_body = {
            "timeStamp": time_stamp,
            "request_status": 1,
            "requestId": 704818,
            "user_system": {
                "user_status": "",
                "system_status": ""
            },
            "ocr_input": {
                "ocr_alldoc_info": "",
                "ocr_keyword_info": [],
                "ocr_alldoc_len": 200,
                "ocr_key_info": [],
                "ocr_key_len": 4,
                "ocr_key_info_offset": []
            },
            "asr_input": {
                "asr_len": 30,
                "asr_info": asr_info
            },
            "sessionId": 704818,
            "handle_input": {
                "handle_task_type": handle_task_type
            },
            "imgRecognition_input": {
                "imgRecognition_info": ""
            },
            "userId": 704818,
            "maxProcessTime": 300
        }
        return req_body

    '''
    '''

    def fetch_nlu_single(self, asr_context):
        jsonBody = self.req_builder(asr_info=asr_context)
        r = requests.post(fetchnlu_url, data=json.dumps(jsonBody))
        resDic = r.json()
        # print('raw resDic = ', resDic)
        raw_value = asr_context
        nlu_skill = None
        nlu_task = None
        nlu_result_is_valid = False
        nlu_result_tts_task_type = None
        nlu_result_tts_text = None
        if (r.status_code == 200):
            nlu_skill = resDic['nlu']['skill']
            nlu_task = resDic['nlu']['task']
            nlu_result_is_valid = resDic['NLU_result']['is_valid_result']
            nlu_result_tts_task_type = resDic['NLU_result']['task_type']
            nlu_result_tts_text = resDic['NLU_result']['tts_text']
        return raw_value, nlu_skill, nlu_task, nlu_result_is_valid, nlu_result_tts_task_type, nlu_result_tts_text

    def fetch_nlu_batch(self):
        title_dict = ["raw_value", "nlu_skill", "nlu_task", "nlu_result_is_valid", "nlu_result_tts_task_type",
                      "nlu_result_tts_text"]
        # title_dict_question_detail = ["module_id", "question", "isCalc", "code", "msg", "video_url"]
        qDict = self._read_query("hotwords.csv")
        # {'code': 0, 'msg': 'success', 'data': {'is_calc': False, 'video_url': '', 'module_id': ''}
        res_file = "data/hotwords_output.csv"
        # question_detail_file = "result/wordproblem_question_detail_v20211021.csv"
        try:
            with open(res_file, 'a+') as df:
                csv.writer(df, lineterminator='\n').writerow(title_dict)

            # with open(question_detail_file, 'a+') as qdf:
            #     csv.writer(qdf, lineterminator='\n').writerow(title_dict_question_detail)
        except RuntimeError as e:
            pass

        for i in range(0, len(qDict)):
            try:
                context = self.fetch_nlu_single(qDict[i][0])
                print("context = " + str(context))
                with open(res_file, 'a+') as df:
                    csv.writer(df, lineterminator='\n').writerow(context)

                # with open(question_detail_file, 'a+') as qf:
                #     csv.writer(qf, lineterminator='\n').writerow(" ".join(str(res) for res in context))
            except RuntimeError as e:
                # logger.error(e)
                pass

    def _read_query(self, csvFile):
        qDict = []
        try:
            with open("data/" + csvFile, 'r') as f1:
                qList = f1.readlines()
                if (len(qList) > 1):
                    for i in range(1, len(qList)):
                        p_ = qList[i]
                        p1_ = p_.replace("\n", "")
                        p_detal_dict_ = p1_.split('\t')
                        qDict.append(tuple(p_detal_dict_))
                        # print("p_detail_dict_ = " + str(p_detal_dict_))
        except RuntimeError as err:
            pass

        # print("inputQDict = " + str(qDict))
        return qDict

    # 生成字符串
    def str_create(self):
        strnew = appSecret + "X-Alv-Timestamp=" + time_stamp + "&X-Alv-Nonce=" + x_xlv_nonce \
                 + "&X-Alv-AppKey=" + appKey
        # print(strnew)
        return strnew

    # 生成signature
    def signature_create(self):
        str_switch = self.str_create()
        # signature = hashlib.sha1(str_switch.encode('utf-8')).hexdigest().lower().strip()
        signature = self.signature_create_via_md5(str_switch)
        # print("signature=" + signature)
        return signature

    # 生成signature
    def signature_create_via_md5(self, str_switch):
        # signature = hashlib.sha1(str_switch.encode('utf-8')).hexdigest().lower().strip()
        md5 = hashlib.md5()
        md5.update(str_switch.encode('utf-8'))
        signature = md5.hexdigest()
        # print("signature=" + signature)
        return signature

    # # 生成token
    # def token_create(self):
    #     signature = self.signature_create()
    #     params = {"appKey": appKey, "timestamp": time_stamp, "signature": signature}
    #     res = requests.get(url=url, params=params)
    #     print(res.url)
    #     print(json.loads(res.content.decode('utf-8')))
    #     token = json.loads(res.content.decode('utf-8'))['result']['token']  # 字节型的response转换成字符串型，再转换成字典型
    #     print(token)
    #     return token


if __name__ == '__main__':
    tc = ApplicationAutoDemo()
    # tc.check_question_context()

    start_time = time.time()
    # print("start_time = " + str(start_time))
    # print(tc._read_query('baike.csv'))
    # print(tc.fetch_nlu_single('精神损失'))
    # print("fetchnlu_url=", fetchnlu_url)

    # queryDict = ['这道题怎么解','这道题怎么算','教我这道题','告诉我这道题','我要问这道题','这道题做法是什么']
    # queryDict = ['现在几点了','今天几号','今天星期几','现在时间','今天是周六吗']

    #  nlu 1.6
    # queryDict = [ '一个苹果怎么写','冷是前鼻音吗', '你好吗', '一年级的年怎么写',
    #              '精神损失', '纬编','花着','湿纸巾','零售价',
    #              '我的属相是马','歌手李娜的代表作','  故宫的面积有多大','  介绍一下姚明' ]
    # queryDict = ['精神损失', '纬编','花着','湿纸巾','零售价']

    #  nlu 1.7
    # queryDict = [ '你好啊', '你好吗', '你好吗', '早上好']  #
    # queryDict = ['语音留言','视频通话','学习任务','名师课堂','学而思教辅','分级阅读','延时关灯','模式切换','提交作业','检查作业','魔法盒']
    # queryDict = ['帮我接通视频通话','打个视频通话']
    # queryDict = ['较暗','教案','较亮','较量','升高','身高']
    # queryDict = ['较暗','教案','较亮','较量','升高','身高','把灯调到教案','身高音量','把灯调到较量','开灯并调整到较亮']
    # queryDict = ['播放蝉','浪花赋予人的情感','好吧好吧','答错了'] # 无数据词语
    # queryDict = ['冬天的词语','包含冬天的词语有哪些','包含冬天的成语有哪些','以好的开关的词语有哪些','好的词语有哪些','任务组词','包含任务的成语有哪些','包括前程词语有哪些','天字组词','山的词语',
    #              '雪的词语','风的词语','雨的词语']

    # queryDict=['风', '雨','风雨交加']
    # queryDict=['风', '雨','风雨交加','注释']

    queryDict = ['今天天气','明天天气',  '北京天气','上海天气', '昌平天气', '武昌天气','朝阳天气','葫芦岛天气','武汉天气', '纽约天气', '燕郊天气']
    # queryDict =  ['第一个字是色的成语有哪些', '形容颜色很多的成语是什么', '形容很高兴的成语怎么说', '表达颜色的字有哪些']
    # queryDict = ['李白写的诗','静夜思的诗']

    for w in queryDict:
        print(tc.fetch_nlu_single(w))

    # print(tc.fetch_nlu_batch())
    # tc.push_question_context()
    # tc.query_res_question_context()
    end_time = time.time()
    duration = end_time - start_time
    print("Elapsed time = " + str(duration))
    # duration = 197.27643394470215
