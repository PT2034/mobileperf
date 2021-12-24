"""
Created on 2021年10月15日
@author: lz

接口wiki
https://wiki.zhiyinlou.com/pages/viewpage.action?pageId=165592500
服务端接口验签说明
https://wiki.zhiyinlou.com/pages/viewpage.action?pageId=155238223

host
http://ailearn.chengjiukehu.com/alv-automath-service-web
接口地址
/v1/application/res

"""
import csv
import time
import hashlib
import uuid
from datetime import datetime

import requests
import operator
import json

from sample.data_processor_utils_v2.CSVUtil import CSVUtil

appKey = "Q93a36gZ"
# appSecret = "fc4ec0c2c4dfd2dbabbe42dee4562822"
appSecret = "zuNhL4db4e1kzZJcob7Bj5Kn51T0z3ms"
time_stamp = str(int(time.time()))
# auth = ('ims', 'ims123')
x_xlv_nonce_uuid = str(uuid.uuid4())
x_xlv_nonce=''.join(x_xlv_nonce_uuid.split('-'))

test_baseurl = "https://ailearn.chengjiukehu.com/alv-automath-service-web"
check_question_api = test_baseurl + "/v1/application/check"
push_question_api = test_baseurl + "/v1/application/push"
query_res_question_api = test_baseurl + "/v1/application/res"

class ApplicationAutoDemo():
    def __init__(self):
        self.headers = {'content-type': 'application/json;charset=utf-8',
                        'X-Alv-Timestamp': time_stamp,
                        'X-Alv-Nonce': x_xlv_nonce,
                        'X-Alv-AppKey': appKey,
                        'X-Alv-Sign': self.signature_create()}

    # 1. /v1/application/check  检测题目是否可解
    def check_question_context(self,question):
        # signature = self.signature_create()
        # params = {"appKey": appKey, "timestamp": time_stamp, "signature": signature}
        # jsonBody = {"question": "一桶油重7.5kg，用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg，一共需要准备几个这样的塑料瓶？"}
        # question = "一桶油重7.5kg，用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg，一共需要准备几个这样的塑料瓶？"
        jsonBody = {"question": question}

        r = requests.post(url=check_question_api, headers=self.headers, data=json.dumps(jsonBody))
        # print(res.url)
        # print(self.headers)
        # print(json.loads(res.content.decode('utf-8')))

        resDic = r.json()
        # print(raw_question_context,r.status_code,resDic['code'], resDic['trace_id'], \
        #        resDic['data']['is_calc'],resDic['data']['video_url'],resDic['data']['pre_process_res'],resDic['data']['result'])
        if (r.status_code != 200):
            return str(jsonBody), "status code exception, %s" % r.status_code
        isCalc_ = None
        video_url_ = None
        module_id_ = None
        if (resDic['code'] == 0):
            module_id_ = resDic['data']['module_id']
            isCalc_ = resDic['data']['is_calc']
            video_url_ = resDic['data']['video_url']

        return module_id_, resDic['code'], resDic['msg'], \
               isCalc_, video_url_

    def check_question_context_batch(self):
        title_dict = ["module_id", "code", "msg", "isCalc", "video_url"]
        qDict = CSVUtil.read_questions("wordproblem_qlist.csv")
        # {'code': 0, 'msg': 'success', 'data': {'is_calc': False, 'video_url': '', 'module_id': ''}
        res_file = "result/wordproblem_res222.csv"
        try:
            with open(res_file, 'a+') as df:
                csv.writer(df, lineterminator='\n').writerow(title_dict)
        except RuntimeError as e:
            pass

        for i in range(0, len(qDict)):
            try:
                with open(res_file, 'a+') as df:
                    context = self.check_question_context(qDict[i])
                    print("context = " + str(context))
                    csv.writer(df, lineterminator='\n').writerow(context)
            except RuntimeError as e:
                # logger.error(e)
                pass

    # 2./v1/application/push 发起解题任务
    def push_question_context(self):
        # signature = self.signature_create()
        # params = {"appKey": appKey, "timestamp": time_stamp, "signature": signature}
        jsonBody = {"module_id": "1007428", "question": "一桶油重7.5kg，用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg，一共需要准备几个这样的塑料瓶？"}
        res = requests.post(url=push_question_api, headers=self.headers, data=json.dumps(jsonBody))
        # print("jsonBody = " + str(jsonBody))
        # print("res.url = " + res.url)
        # print("headers = " + str(self.headers))

        print(json.loads(res.content.decode('utf-8')))
        # token = json.loads(res.content.decode('utf-8'))['query']['token']  # 字节型的response转换成字符串型，再转换成字典型
        # print(token)
        # return token

    # 3./v1/application/res 获取解题结果
    def query_res_question_context(self):
        # signature = self.signature_create()
        # params = {"appKey": appKey, "timestamp": time_stamp, "signature": signature}
        jsonBody = {"module_id": "1007428", "question": "一桶油重7.5kg，用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg，一共需要准备几个这样的塑料瓶？"}
        res = requests.post(url=query_res_question_api, headers=self.headers, data=json.dumps(jsonBody))
        print(json.loads(res.content.decode('utf-8')))
        # token = json.loads(res.content.decode('utf-8'))['query']['token']  # 字节型的response转换成字符串型，再转换成字典型
        # print(token)
        # return token

    # 生成字符串
    def str_create(self):
        strnew = appSecret +"X-Alv-Timestamp=" + time_stamp + "&X-Alv-Nonce=" + x_xlv_nonce \
                 + "&X-Alv-AppKey=" + appKey
        print(strnew)
        return strnew

    # 生成signature
    def signature_create(self):
        str_switch = self.str_create()
        # signature = hashlib.sha1(str_switch.encode('utf-8')).hexdigest().lower().strip()
        signature= self.signature_create_via_md5(str_switch)
        print("signature=" + signature)
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
    # print( tc.check_question_context_batch())
    tc.push_question_context()
    tc.query_res_question_context()
    end_time = time.time()
    duration = end_time - start_time
    print("duration = " + str(duration))
    # res111
    # duration = 197.27643394470215

    # res222
    # duration =

    # str_create()
    # signature_create()
    # tc.token_create()
    # tc.str_create()
    # tc.signature_create()
