# -*- encoding:utf-8 -*-

import os
import time
import json
import random
import config
import requests
import pandas as pd
from loguru import logger


def write_excel(dict_content, basename):
    new_xlsx_file = os.path.join(os.getcwd(), "smoke_result_"+os.path.splitext(basename)[0]+'.xlsx')
    df = pd.DataFrame(dict_content)
    df.to_excel(new_xlsx_file, header=True, index=False)


def generate_zici_request_body(asr_info):
    """
    :param
        asr_info: 请求nlu接口的语音文本内容
    """
    user_id = random.randint(100, 100000)
    # 13位时间戳
    timestamp = int(round(time.time() * 1000))
    # request_data = copy.deepcopy(config.request_data)
    request_data = config.request_data
    request_data["userId"] = user_id
    request_data["requestId"] = user_id
    request_data["sessionId"] = user_id
    request_data["timeStamp"] = timestamp
    request_data["asr_input"]["asr_info"] = asr_info

    return request_data


def generate_finger_request_body(ocr_key_info_tmp, ocr_keyword_info_tmp,
                                ocr_key_info_offset_tmp, handle_task_type_tmp):
    """
    :param ocr_key_info_tmp:
    :param ocr_keyword_info_tmp:
    :param ocr_key_info_offset_tmp:
    :param handle_task_type_tmp:
    :return:
    """
    user_id = random.randint(100, 100000)
    # 13位时间戳
    timestamp = int(round(time.time() * 1000))
    request_data = config.request_data
    request_data["userId"] = user_id
    request_data["requestId"] = user_id
    request_data["sessionId"] = user_id
    request_data["timeStamp"] = timestamp
    request_data["asr_input"]["asr_info"] = ""
    request_data["ocr_input"]["ocr_key_info"] = ocr_key_info_tmp
    request_data["ocr_input"]["ocr_keyword_info"] = ocr_keyword_info_tmp
    request_data["ocr_input"]["ocr_key_info_offset"] = ocr_key_info_offset_tmp
    request_data["handle_input"]["handle_task_type"] = handle_task_type_tmp

    return request_data


def send_request(url, data):
    nlu_res = requests.post(url, data=json.dumps(data))

    try:
        string = (json.loads(nlu_res.text))
        logger.info(json.dumps(string))
        ttx_text = string['NLU_result']['tts_text']
        logger.info(ttx_text)
        return ttx_text
    except Exception as e:
        logger.error("解析nlu结果出错: {} - {}".format(repr(e), nlu_res.text))
        return None
