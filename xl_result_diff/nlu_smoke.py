# -*- encoding:utf-8 -*-

"""
nlu自动化冒烟
"""

import os
import re
import sys
import utils
import config
import finger_check
import pandas as pd
from loguru import logger


def parse_zici_xlsx(file_path):
    """ 解析字词Excel标注数据 """
    df = pd.read_excel(file_path, keep_default_na=False)
    # print(df.shape) # 获取数据的总行数、总列数，返回的是元组(行，列)
    data = pd.DataFrame(df)
    # df.shape(0)

    _dict = {}
    _query = {}
    _template_dict = {}
    _expect_result_dict = {}
    _real_result_dict = {}
    _result_bool_dict = {}

    for row in range(df.shape[0]):
        # 读取Excel里的query
        query = data.loc[row]['Query']

        # 读取Query对应的模板
        _template_result = data.loc[row]['TTS模板']

        _query.setdefault("Query", []).append(query)
        _template_dict.setdefault("TTS模板", []).append(_template_result)

        body = utils.generate_zici_request_body(query)

        # 调用NLU接口获取nlu返回内容
        if sys.argv[1] == 'online_env':
            tts_text = utils.send_request(config.online_url, body)
        elif sys.argv[1] == 'test_env':
            tts_text = utils.send_request(config.test_url, body)
        else:
            tts_text = utils.send_request(config.test_url, body)

        if (tts_text.strip() in config.baseline_talk) or \
                (tts_text.strip().startswith("小猴没找到")) or \
                (tts_text.strip().startswith("小猴没有找到")) or \
                (tts_text.strip().startswith("小猴不知道")):
            # 判断是否是兜底话术
            match_result = "兜底话术"
        elif '{pattern}' in _template_result:
            _new = _template_result.replace('{pattern}', '.*')
            logger.debug(_new)
            pattern = re.compile(r'%s' % _new)
            try:
                match = re.match(pattern, tts_text)
                match_result = match.group()
            except Exception as e:
                # 正则匹配失败
                logger.error(repr(e))
                match_result = "正则匹配失败"
        else:
            match_result = _template_result

        if match_result == tts_text:
            _result_bool_dict.setdefault("是否与预期一致", []).append("是")
        else:
            _result_bool_dict.setdefault("是否与预期一致", []).append("否")

        # _expect_result_dict.setdefault("模板匹配结果", []).append(match_result)
        _real_result_dict.setdefault("接口返回结果", []).append(tts_text)


    _dict.update(_query)
    _dict.update(_template_dict)
    # _dict.update(_expect_result_dict)
    _dict.update(_real_result_dict)
    _dict.update(_result_bool_dict)

    base_name = os.path.basename(file_path)
    utils.write_excel(_dict, base_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    logger.add("nlu_smoke.log", level="INFO")
    query_file_path = os.path.join(os.getcwd(), 'data')
    for file_name in os.listdir(query_file_path):
        if os.path.splitext(file_name)[1] == '.xlsx':
            if file_name == '指令_字词.xlsx':
                parse_zici_xlsx(os.path.join(query_file_path, file_name))
                pass
            elif file_name == "指查_指读.xlsx":
                finger_check.parse_finger_xlsx(os.path.join(query_file_path, file_name))
                pass
