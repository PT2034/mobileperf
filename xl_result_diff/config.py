# -*- encoding:utf-8 -*-

# 兜底话术
baseline_talk = [
    "抱歉，小猴没听清。",
    "抱歉，小猴没听懂。",
    "抱歉，小猴没理解。",
    "抱歉，小猴答不上来",
    "我们先不要聊天啦，好好学习吧！",
]


""" nlu接口 """
test_url = "http://hmi-in.chengjiukehu.com/monkey-light-demo/fetchnlu"   # 测试环境
online_url = "http://t-talk.vdyoo.net/monkey-light-demo/fetchnlu"     # 线上环境公网调试专用


""" nlu接口请求报文 """
request_data = {
    # 用户id
    "userId": "",
    # 请求id
    "requestId": "",
    # 会话id
    "sessionId": "",
    # 时间戳
    "timeStamp": "",
    # 最大请求响应时间，毫秒级别
    "maxProcessTime": 300,
    # 请求状态，比如指定是否返回contentUrl，或指定只走某一路召回
    "request_status": 1,
    # 输入包含用户画像以及系统状态等环境信息，具体内容待明确
    "user_system": {
        "user_status": "",
        "system_status": ""
    },
    "asr_input": {
        # 输入语音识别文本长度
        "asr_len": "",
        # 输入语音识别文本信息
        "asr_info": ""
    },
    "ocr_input": {
        # 输入ocr识别文本长度
        "ocr_alldoc_len": 200,
        # 划词时滑动的字符长度
        "ocr_key_len": 4,
        # ocr识别到的全部文本，如果有的话
        "ocr_alldoc_info": "",
        # ocr识别到的行文本字符串
        # "ocr_key_info": ['见仁见智'],
        "ocr_key_info": [],
        # 识别到的指尖指向的关键字,0-2个元素
        #"ocr_keyword_info": ['见仁见智'],
        "ocr_keyword_info": [],
        # 指尖所指的字符在行文本中的偏移量，0-2个元素
        "ocr_key_info_offset": []
    },
    "handle_input": {
        # 用户当前操作行为意图
        "handle_task_type": "",
    },
    "imgRecognition_input": {
        # 输入图像识别
        "imgRecognition_info": ""
    }
}
