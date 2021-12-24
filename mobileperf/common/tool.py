import time
import os


def get_root_path():
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.abspath(os.path.dirname(curPath) + os.path.sep + ".") + '/'
    return rootPath

'''
   判断一个时间是否在指定的时间段之间（时间段可以是多个时间段）
'''
def is_time_between_period_time(periods, current_time):
    state = 0
    # 如果要判断的时间为空，返回0
    if current_time is None or current_time == '0000-00-00 00:00:00':
        return 0
    for period in periods:
        begin = time.strptime(period['begin'], '%Y-%m-%d %H:%M:%S')
        end = time.strptime(period['end'], '%Y-%m-%d %H:%M:%S')
        current = time.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        if begin <= current <= end:
            state = 1
            break

    return state


'''
将一个字符串按指定符合分割，并去除''    
'''


def split_and_remove_none_str(res, dst):
    res = res.split(dst)
    while '' in res:
        res.remove('')
    return res


'''
 将 yyyy-mm-dd/hh:mm:ssandyyyy-mm-dd/hh:mm:ss格式的时间转化为搜索需要的时间格式
'''


def conversion_time_format_jenkins_to_py(periods):
    res = []
    period = split_and_remove_none_str(periods.replace('/', ' '), 'or')
    for i in period:
        i = split_and_remove_none_str(i, '~')
        t = {'begin': str(i[0]), 'end': str(i[1])}
        res.append(t)

    return res


