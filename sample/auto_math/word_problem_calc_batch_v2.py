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



automath_check_sum_api = 'https://qz-test.oss-cn-beijing.aliyuncs.com/word-problem-h5/index.html#/CourseTab?module_id=%s&question=%s'

def question_url_builder(raw_question_context_dict):
    url = build_question_check_url(raw_question_context_dict)
    print("url=\n",url)
    return raw_question_context_dict[1], raw_question_context_dict[0], url



def question_calc(raw_question_context_dict):
    url = build_question_check_url(raw_question_context_dict)
    print("url=\n",url)
    try:
        r = requests.get(url, auth=auth, headers=headers, verify=False)
    except:
        return raw_question_context_dict, "unknown error"
    # resDic = json.loads(r.json())
    print(r.status_code)
    print(r.text)
    print("r.json()=",r.json())
    resDic = r.json()
    # print(raw_question_context,r.status_code,resDic['code'], resDic['trace_id'], \
    #        resDic['data']['is_calc'],resDic['data']['video_url'],resDic['data']['pre_process_res'],resDic['data']['result'])
    if (r.status_code != 200):
        return raw_question_context_dict, "status code exception, %s" % r.status_code
    isCalc_ = None
    video_url_ = None
    pre_process_res_ = None
    data_result_ = None
    if (resDic['code'] == 0):
        isCalc_ = resDic['data']['is_calc']
        video_url_ = resDic['data']['video_url']
        pre_process_res_ = resDic['data']['pre_process_res']
        data_result_ = resDic['data']['result']
    return r.status_code, resDic['code'], resDic['msg'],resDic['trace_id'], raw_question_context_dict, \
           isCalc_, video_url_, pre_process_res_, data_result_, url

    # return r.json()


def build_question_check_url(raw_question_context_dict):
    
    question_context = urllib.parse.quote(raw_question_context_dict[0], encoding='utf-8')
    url = automath_check_sum_api % (raw_question_context_dict[1], question_context)
    return url


def resurl_collector(questionDict, qFileName='calc'):
    full_time_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    calc_res_title = ["module_id", "question_context", "playback_url"]
    resFile = 'result/'+qFileName+'res_%s.csv' % full_time_timestamp
    res_file = os.path.join(resFile)
    print("computing...")
    print("congrats, batch calc result has been saved here, %s" % res_file)

    try:
        with open(res_file, 'a+') as df:
            csv.writer(df, lineterminator='\n').writerow(calc_res_title)
    except RuntimeError as e:
        logger.error(e)

    for i in range(0, len(questionDict)):
        try:
            with open(res_file, 'a+') as df:
                csv.writer(df, lineterminator='\n').writerow(question_url_builder(questionDict[i]))
        except RuntimeError as e:
            logger.error(e)


# def pretreat_q(param):
#     param.replace("x", "\\times").replace("X", "\\times")
#     return param


def read_questions(csvFile):
    qDict = []
    try:
        with open("input/"+csvFile, 'r') as f2:
            qList = f2.readlines()
            if (len(qList) >= 1):
                for i in range(1, len(qList)):
                    p_ = qList[i]
                    # p_=pretreat_q(p_)
                    print('p_ =',p_ )
                    p_ = p_.replace("\n", "").replace("\t","")
                    q_desc_ = p_.split('？')
                    q_desc_[0]=q_desc_[0]+'？'
                    q_desc_=[i.strip() for i in q_desc_]
                    qDict.append(q_desc_)
    except RuntimeError as err:
        logger.error(err)

    return qDict


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
    # print(read_questions('wordproblem_qlist.csv'))
    questions= read_questions('wordproblem_qlist.csv')
    # print(question_url_builder(questions[0]))
    # resurl_collector(question_url_builder(questions[0]))
    resurl_collector(questions)

    # print(question_calc('36%C3%9731-26%C3%9743%2B12%C3%9726'))
    # print(question_calc('36×31-26×43+12×26'))
    # print(read_questions())
    # contract_calc_helper('contract_qlist.csv')
    # contract_calc_helper('contract_qlist_assignprinciple_dot.csv')
    # contract_calc_helper('contract_qlist_assignprinciple_dot.csv')