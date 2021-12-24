#!python3
# -*- coding: utf-8 -*-
import platform
#print(platform.python_version())
import oss2
import sys
import os
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import config
import generate_json

current_dir_abs = os.path.abspath(os.path.dirname(__file__))

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth(config.accessKeyId, config.accessKeySecret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, config.endpoint, config.bucketName)

per_int = 0
def _percentage(consumed_bytes, total_bytes):
    global per_int
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        if rate//10 > per_int:
            print('\r{0}% '.format(rate), end='')
            sys.stdout.flush()
            per_int=rate//10

def _check_md5(local_file, remote_md5):
    local_md5 = generate_json.get_file_md5(local_file)
    return local_md5 == remote_md5.lower()

#便捷上传
def simple_upload(abs_file_path, parent_dir):
    '''上传指定文件到OSS
    Args:
        abs_file_path (str): The path of the file to upload
        parent_dir (str): 上传到oss时的外层目录，在objectRootName和filename之间，一般是版本号如https://xxxx.xesimg.com/Android/appVersion/$parent_dir/filename.apk
    '''
    global per_int
    if parent_dir is None or parent_dir == "" :
        print("外层文件夹不能为空，一般是版本号")
        sys.stdout.flush()
        return
    file_name = os.path.basename(abs_file_path)
    objectName = os.path.join(config.objectRootName, parent_dir, file_name)
    log_pre = f"上传文件:{file_name}到{objectName}，百分比:"
    print(log_pre, end='')
    #初始化百分比
    per_int = 0
    putObjectResult = bucket.put_object_from_file(objectName, abs_file_path, progress_callback=_percentage)
    #print('http status: {0}'.format(putObjectResult.status))
    #print('etag: {0}'.format(putObjectResult.etag))
    #增加验证回传的ETAG是否与本地文件MD5一致，以确定确实上传成功
    if not _check_md5(abs_file_path, putObjectResult.etag):
        raise Exception("md5 与本地文件不一致，请检查")
    print()
    sys.stdout.flush()

def walk_upload(relative_dir, parent_dir):
    '''遍历文件夹内容并上传【网校安卓版】
    Args:
        relative_dir (str): The path of the directory to walk_upload
    '''
    if parent_dir is None or parent_dir == "" :
        print("版本号作为外层文件夹，不能为空")
        sys.stdout.flush()
        return
    for root, dirs, files in os.walk(os.path.join(current_dir_abs, relative_dir), topdown=False):
        print(f"共有{len(files)}个文件")
        i = 1
        for name in files:
            print(f"正在上传第{i}个文件")
            sys.stdout.flush()
            simple_upload(os.path.abspath(os.path.join(root, name)), parent_dir)
            i += 1
        print("全部上传完成")
        sys.stdout.flush()

#python3 upload_channel_apk.py ${parent_dir}
if __name__ == "__main__":
    #simple_upload(os.path.join(current_dir_abs, "release-8.02.01_aligned.apk"))
    walk_upload("channels", sys.argv[1])
