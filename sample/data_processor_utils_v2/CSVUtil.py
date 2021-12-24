import csv
import logging

logger = logging.getLogger('data_processor_utils_v2')


class CSVUtil():
    def read_questions(csvFile):
        qDict = []
        try:
            with open("input/" + csvFile, 'r') as f2:
                qList = f2.readlines()
                if (len(qList) >1 ):
                    for i in range(1, len(qList)):
                        p_ = qList[i]
                        p1_=p_.replace("\n", "")
                        p_detal_dict_ = p1_.split('\t')
                        qDict.append(tuple(p_detal_dict_))
                        # print("p_detail_dict_ = " + str(p_detal_dict_))
        except RuntimeError as err:
            logger.error(err)

        # print("inputQDict = " + str(qDict))
        return qDict

    def read_moduleid(csvFile):
        qDict = []
        try:
            with open("input/" + csvFile, 'r') as f2:
                qList = f2.readlines()
                if (len(qList) >1 ):
                    for i in range(1, len(qList)):
                        p_ = qList[i]
                        qDict.append(p_.replace("\n", ""))
        except RuntimeError as err:
            logger.error(err)

        # print("inputQDict = " + str(qDict))
        return qDict

    def write_result(res_file, res_title, res_dict):
        try:
            with open("result/" + res_file, 'a+') as df:
                csv.writer(df, lineterminator='\n').writerow(res_title)
        except RuntimeError as e:
            logger.error(e)

        for i in range(0, len(res_dict)):
            try:
                with open(res_file, 'a+') as df:
                    csv.writer(df, lineterminator='\n').writerow(res_dict[i])
            except RuntimeError as e:
                logger.error(e)


if __name__ == '__main__':
    # title_dict = ["module_id", "code", "msg", "isCalc","video_url"]
    CSVUtil.read_questions("wordproblem_qlist_detail.csv")

    # {'code': 0, 'msg': 'success', 'data': {'is_calc': False, 'video_url': '', 'module_id': ''}
    # CSVUtil.write_result("wordproblem_res111.csv",title_dict , " ")
