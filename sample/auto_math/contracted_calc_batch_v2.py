# coding=utf-8
"""
Created on Oct 12, 2021
"""
import csv
import logging
import threading
import time

import requests
import json
import urllib
import os

logger = logging.getLogger('videoquestion')

headers = {'content-type': 'application/json'}
auth = ('test', '123456')

automath_check_baseurl = 'http://ailearn.chengjiukehu.com/alv-automath-service-web/v1/automath/check'
automath_check_sum_api = 'http://ailearn.chengjiukehu.com/alv-automath-service-web/v1/automath/check?sum=%s'


def question_calc(raw_question_context):
    url = build_question_check_url(raw_question_context)
    try:
        r = requests.get(url, auth=auth, headers=headers, verify=False)
    except:
        return raw_question_context, "unknown error"
    # resDic = json.loads(r.json())
    resDic = r.json()
    # print(raw_question_context,r.status_code,resDic['code'], resDic['trace_id'], \
    #        resDic['data']['is_calc'],resDic['data']['video_url'],resDic['data']['pre_process_res'],resDic['data']['result'])
    if (r.status_code != 200):
        return raw_question_context, "status code exception, %s" % r.status_code
    isCalc_ = None
    video_url_ = None
    pre_process_res_ = None
    data_result_ = None
    if (resDic['code'] == 0):
        isCalc_ = resDic['data']['is_calc']
        video_url_ = resDic['data']['video_url']
        pre_process_res_ = resDic['data']['pre_process_res']
        data_result_ = resDic['data']['result']
    return r.status_code, resDic['code'], resDic['msg'],resDic['trace_id'], raw_question_context, \
           isCalc_, video_url_, pre_process_res_, data_result_, url

    # return r.json()


def build_question_check_url(raw_question_context):
    question_context = urllib.parse.quote(raw_question_context, encoding='utf-8')
    url = automath_check_sum_api % question_context
    return url


def contract_calc_res_collector(questionDict, qFileName='calc'):
    full_time_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    calc_res_title = ["status_code", "code", "msg", "trace_id", "origin_question"]
    resFile = 'result/'+qFileName+'res_%s.csv' % full_time_timestamp
    res_file = os.path.join(resFile)
    print("computing...")
    print("congrats, batch calc result has been saved here, %s" % res_file)
    calc_res_title.extend(["is_calc", "video_url", "pre_process_res", "result", "full_url"])

    try:
        with open(res_file, 'a+') as df:
            csv.writer(df, lineterminator='\n').writerow(calc_res_title)
    except RuntimeError as e:
        logger.error(e)

    for i in range(0, len(questionDict)):
        try:
            with open(res_file, 'a+') as df:
                csv.writer(df, lineterminator='\n').writerow(question_calc(questionDict[i]))
        except RuntimeError as e:
            logger.error(e)

def pretreat_q(param):
    param.replace("x", "\\times").replace("X", "\\times")
    return param

def read_questions(csvFile):
    qDict = []
    try:
        with open("input/"+csvFile, 'r') as f2:
            qList = f2.readlines()
            if (len(qList) != 0):
                for i in range(0, len(qList)):
                    p_ = qList[i]
                    p_=pretreat_q(p_)
                    qDict.append(p_.replace("\n", ""))
    except RuntimeError as err:
        logger.error(err)

    return qDict


def contract_calc_helper(inputQuestionFile):
    qDict = read_questions(inputQuestionFile)
    contract_calc_res_collector(qDict,qFileName=inputQuestionFile.replace(".csv","_"))


class RuntimeData(object):
    # 记录pid变更前的pid
    old_pid = None
    packages = None
    package_save_path = None
    start_time = None
    exit_event = threading.Event()
    top_dir = None
    config_dic = {}


if __name__ == '__main__':
    # print(question_calc('36%C3%9731-26%C3%9743%2B12%C3%9726'))
    # print(question_calc('36×31-26×43+12×26'))
    # print(read_questions())
    # contract_calc_helper('contract_qlist.csv')
    # contract_calc_helper('contract_qlist_assignprinciple_dot.csv')
    contract_calc_helper('contract_qlist_assignprinciple_dot.csv')