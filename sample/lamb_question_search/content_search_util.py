"""
Created on 2021年10月15日
@author: lz

拍搜服务文字搜题
https://wiki.zhiyinlou.com/pages/viewpage.action?pageId=164887944

Host
测试(外网)：https://qz.chengjiukehu.com/test/qingzhou-search-api
测试(内网)：http://qz-internal.chengjiukehu.com/test/qingzhou-search-api
生产(外网)：https://api.tipaipai.com/tpp-search-api
生产(内网)：http://api-internal.tipaipai.com/tpp-search-api

"""

import time
import hashlib
import uuid

import requests
import json

appKey = "47ea14770d5d0a0ef858557937cbeff9"
appSecret = "123456"

time_stamp = str(int(time.time()))
# auth = ('ims', 'ims123')
x_qz_nonce_uuid = str(uuid.uuid4())
x_qz_nonce=''.join(x_qz_nonce_uuid.split('-'))
test_baseurl = "https://qz.chengjiukehu.com/test/qingzhou-search-api"
question_content_api = test_baseurl + "/search/question/content"


class get_tokenclass():
    def __init__(self):
        self.headers = {'content-type': 'application/json',
                        'X-Qz-Timestamp': time_stamp,
                        'X-Qz-Nonce': x_qz_nonce,
                        'X-Qz-AppKey': appKey,
                        'X-Qz-Sign': self.signature_create()}

    # 生成token
    def q_question_context(self):
        # signature = self.signature_create()
        # params = {"appKey": appKey, "timestamp": time_stamp, "signature": signature}

        # 题型，1 - 计算题 2 - 应用题  0 - 默认(不进行自动视频讲解查询)
        jsonBody = {"words": "22.9-3", "qt": 1}
        res = requests.post(url=question_content_api, headers=self.headers, data=json.dumps(jsonBody))

        print("jsonBody = " + str(jsonBody))
        print("res.url = " + res.url)
        print("headers = " + str(self.headers))
        print(json.loads(res.content.decode('utf-8')))

    # 生成token
    def q_question_context_parameterized(self, words_content, question_type):
        # signature = self.signature_create()
        # params = {"appKey": appKey, "timestamp": time_stamp, "signature": signature}

        # 题型，1 - 计算题 2 - 应用题  0 - 默认(不进行自动视频讲解查询)
        jsonBody = {"words": words_content, "qt": question_type}
        res = requests.post(url=question_content_api, headers=self.headers, data=json.dumps(jsonBody))

        print("jsonBody = " + str(jsonBody))
        print("res.url = " + res.url)
        # print("headers = " + str(self.headers))
        print(json.loads(res.content.decode('utf-8')))

        # token = json.loads(res.content.decode('utf-8'))['query']['token']  # 字节型的response转换成字符串型，再转换成字典型
        # print(token)
        # return token

    # 生成字符串
    def str_create(self):
        strnew = "X-Qz-Timestamp=" + time_stamp + "&X-Qz-Nonce=" + x_qz_nonce \
                 + "&X-Qz-AppKey=" + appKey + "&app_secret=" + appSecret
        print(strnew)
        return strnew

    '''
    md5生成一个128bit的结果，通常用32位的16进制字符串表示
    sha1生成一个160bit的结果，通常用40位的16进制字符串表示
    '''
    # 生成signature
    def signature_create(self):
        str_switch = self.str_create()
        # signature = self.signature_create_via_sha1(str_switch)
        signature = self.signature_create_via_md5(str_switch)
        print("signature=" + signature)
        return signature

    # 生成signature
    def signature_create_via_md5(self, str_switch):
        md5 = hashlib.md5()
        md5.update(str_switch.encode('utf-8'))
        signature = md5.hexdigest()
        # print("signature=" + signature)
        return signature

    # 生成signature
    def signature_create_via_sha1(self, str_switch):
        signature = hashlib.sha1(str_switch.encode('utf-8')).hexdigest().lower().strip()
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
    tc = get_tokenclass()
    # tc.q_question_context()
    # tc.q_question_context_parameterized("22.9-3", 1)
    tc.q_question_context_parameterized("一桶油重7.5kg，用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg，一共需要准备几个这样的塑料瓶？", 2)
    # tc.q_question_context_parameterized(" 4.一桶油重 $$7k_{8}$$ 用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg。一共需要准备几个这样的料瓶?(5分)", 2)
    # tc.q_question_context_parameterized("一桶油重7.5kg，用掉3.7kg后，把剩余的装在塑料瓶中，每瓶最多可装0.9kg，一共需要准备几个这样的塑料瓶？", 0)
    # str_create()
    # signature_create()
    # tc.token_create()
    # tc.str_create()
    # tc.signature_create()
