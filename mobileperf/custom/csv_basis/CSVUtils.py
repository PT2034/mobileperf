import os
import sys
import csv

'''
reference: 
https://blog.csdn.net/zly412934578/article/details/80844674
'''

class CSV_Utils:
    '''
    利用python中csv模块读写文件(筛选特定的列)
    '''
    @classmethod
    def query_row_by_column_name(cls,input_file, output_file):
        # input_file=sys.argv[1]
        # output_file=sys.argv[2]
        '''第二种：根据列标题选出特定的列
                注：方法和第一种的区别在在于，先根据列标题找出列索引，然后在运用第一种方法读写文件，好处是列标题是固定的
        '''
        my_columns = ['module_id', 'isCalc']
        my_columns_index = []
        with open(input_file, 'r', newline='') as csv_in_file:
            with open(output_file, 'w', newline='') as csv_out_file:
                filereader = csv.reader(csv_in_file)  # 将csv文件的每行以列表的形式返回
                filewriter = csv.writer(csv_out_file)  # 创建一个写入对象，delimiter是默认分隔符
                header = next(filereader, None)
                for index_value in range(len(header)):
                    if header[index_value] in my_columns:
                        my_columns_index.append(index_value)
                filewriter.writerow(my_columns)
                for row_list in filereader:
                    row_list_output = []
                    for index_value in my_columns_index:
                        row_list_output.append(row_list[index_value])
                filewriter.writerow(row_list_output)

    '''    
    利用python中csv模块读写文件(筛选特定的列)
    '''
    @classmethod
    def query_row_by_index(cls,input_file, output_file):
        # input_file=sys.argv[1]
        # output_file=sys.argv[2]

        with open(input_file, 'r', newline='') as csv_in_file:
            with open(output_file, 'w', newline='') as csv_out_file:
                filereader = csv.reader(csv_in_file)  # 将csv文件的每行以列表的形式返回
                filewriter = csv.writer(csv_out_file)  # 创建一个写入对象，delimiter是默认分隔符
                # 先处理第一行
                header = next(filereader)
                filewriter.writerow(header)
                # 再处理剩余所有行
                for row_list in filereader:
                    supplier = str(row_list[0]).strip()
                    cost = str(row_list[3]).strip("$").replace(',', '')
                    if supplier == 'Supplier Z' or float(cost) > 600.00:
                        filewriter.writerow(row_list)

if __name__ == '__main__':
    root_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
    input_file = root_path + '/input/wordproblem_res_v20211021.csv'
    output_file = root_path+ '/output/logcat_2021_10_19_2.log'
    print(output_file)

    CSV_Utils.query_row_by_column_name(input_file, output_file)

