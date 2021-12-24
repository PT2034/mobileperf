# -*- encoding:utf-8 -*-

import os
import re
import sys
import utils
import config
import pandas as pd
from loguru import logger


def parse_finger_xlsx(file_path):
    """ 解析指查、指读Excel标注数据 """
    df = pd.read_excel(file_path, keep_default_na=False)
    data = pd.DataFrame(df)

    intention_classify = {}
    ocr_key_info = {}
    ocr_keyword_info = {}
    ocr_key_info_offset = {}
    handle_task_type = {}
    tts_task_type = {}
    tts_text_template ={}
    tts_text = {}
    _result_bool_dict = {}
    _real_result_dict = {}

    #df.shape(0)
    for row in range(df.shape[0]):
        intention_classify_tmp = data.loc[row]['intention_classify']
        ocr_key_info_tmp = data.loc[row]['ocr_key_info']
        ocr_keyword_info_tmp = data.loc[row]['ocr_keyword_info']
        ocr_key_info_offset_tmp = data.loc[row]['ocr_key_info_offset']
        handle_task_type_tmp = data.loc[row]['handle_task_type']
        _template_result = data.loc[row]['TTS模板']

        new_ocr_key_info = eval(ocr_key_info_tmp)
        new_ocr_keyword_info = eval(ocr_keyword_info_tmp)
        new_ocr_key_info_offset = eval(ocr_key_info_offset_tmp)

        intention_classify.setdefault("intention_classify", []).append(intention_classify_tmp)
        ocr_key_info.setdefault("ocr_key_info", []).append(new_ocr_key_info)
        ocr_keyword_info.setdefault("ocr_keyword_info", []).append(new_ocr_keyword_info)
        ocr_key_info_offset.setdefault("ocr_key_info_offset", []).append(new_ocr_key_info_offset)
        handle_task_type.setdefault("handle_task_type", []).append(handle_task_type_tmp)
        tts_text_template.setdefault("TTS模板", []).append(_template_result)

        body = utils.generate_finger_request_body(new_ocr_key_info, new_ocr_keyword_info,
                                                  new_ocr_key_info_offset, handle_task_type_tmp)
        # 调用NLU接口获取nlu返回内容
        if sys.argv[1] == 'online_env':
            result_tmp = utils.send_request(config.online_url, body)
        elif sys.argv[1] == 'test_env':
            result_tmp = utils.send_request(config.test_url, body)
        else:
            result_tmp = utils.send_request(config.test_url, body)

        tts_text.setdefault("接口返回结果", []).append(result_tmp)

        if (result_tmp.strip() in config.baseline_talk) or \
                (result_tmp.strip().startswith("小猴没找到")) or \
                (result_tmp.strip().startswith("小猴没有找到")) or \
                (result_tmp.strip().startswith("小猴不知道")):
            # 判断是否是兜底话术
            match_result = "兜底话术"
        elif '{pattern}' in _template_result:
            _new = _template_result.replace('{pattern}', '.*')
            logger.debug(_new)
            pattern = re.compile(r'%s' % _new)
            try:
                match = re.match(pattern, result_tmp)
                match_result = match.group()
            except Exception as e:
                # 正则匹配失败
                logger.error(repr(e))
                match_result = "正则匹配失败"
        else:
            match_result = _template_result

        if match_result == result_tmp:
            _result_bool_dict.setdefault("是否与预期一致", []).append("是")
        else:
            _result_bool_dict.setdefault("是否与预期一致", []).append("否")


    _dict = {}
    _dict.update(intention_classify)
    _dict.update(ocr_key_info)
    _dict.update(ocr_keyword_info)
    _dict.update(ocr_key_info_offset)
    _dict.update(handle_task_type)
    # _dict.update(tts_task_type)
    _dict.update(tts_text_template)
    _dict.update(tts_text)
    _dict.update(_result_bool_dict)

    base_name = os.path.basename(file_path)
    utils.write_excel(_dict, base_name)
