#!/usr/bin/python3
'''
利用python普通模块是实现读写csv文件
步骤1:取出A文件的第一行，去除空格，换行符等符号
步骤2：将A文件的第一行保存到一个列表中，然后写入到B文件中
步骤3：依次循环A文件后面的各行，然后写入到B文件中
'''

import sys
import os

# input_file=sys.argv[1]
# output_file=sys.argv[2]
root_path = os.path.abspath(os.path.join(os.getcwd(), '../..'))
# input_file = 'custom/input/logcat_1.log'
input_file = root_path+ '/results/com.tal.genie.voice/2021_10_19_20_19_54/logcat_2021_10_19_20_19_59.log'
print(input_file)
output_file = 'output/logcat_2021_10_19_2.log'

def query_data():
    with open(input_file, 'r', newline='') as  filereader:
        with open(output_file, 'w', newline='') as filewrite:
            print("writing line...")
            for line in filereader:
            # line = filereader.readline()
                if line.find("cv处理") != -1:
                    print(line)
                    filewrite.write(line)
                    # filewrite.writelines(header)
        print("done")


def func_copy_data():
    with open(input_file, 'r', newline='') as  filereader:
        with open(output_file, 'w', newline='') as filewrite:
            header = filereader.readline()
            header = header.strip()
            header_list = header.split(',')
            print(header_list)
            filewrite.write(','.join(map(str, header_list)) + '\n')
            for row in filereader:
                row = row.strip()
                row_list = row.split(',')
                print(row_list)
                filewrite.write(','.join(map(str, row_list)) + '\n')


if __name__ == '__main__':
    query_data()