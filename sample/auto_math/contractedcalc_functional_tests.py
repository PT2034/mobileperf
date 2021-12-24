# coding=utf-8
"""
Created on Oct 12, 2021
"""
import os
import time
import unittest

from HTMLTestRunner import HTMLTestRunner

from ccalc_utils import question_calc_request

'''
(200, 0, 'success', '2f9a456b19816e4f', '234\\times568', True, 
'https://ailearn.chengjiukehu.com/auto-math-lecture-h5/#/?calc=true&circLen=0&cmpByDot=false&num1=234&num2=568&op=%C3%97&relSym=%3D&validLen=0', 
'{"calc":true,"num1":"234","op":"×","num2":"568","relSym":"=","cmpByDot":false,"validLen":0,"result":"132912","circLen":0}', 
'132912', 'http://ailearn.chengjiukehu.com/alv-automath-service-web/v1/automath/check?sum=234%5Ctimes568')
'''

class ContractedCalcTestsCollector(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("execute setUpClass")

    @classmethod
    def tearDownClass(self):
        print("execute tearDownClass")

    def test_questiontext_normal(self):
        ret = question_calc_request("234\\times568")
        self.assertTrue(ret[1] == 0, "actural code: %s, msg: %s"%(ret[1], ret[2]))

    # actural code: 30004, msg: python接口状态码异常
    def test_questiontext_blank(self):
        ret=question_calc_request(" ")
        self.assertTrue(ret[1] == 30004, "actural code: %s, msg: %s"%(ret[1], ret[2]))

    # actural code: 30004, msg: python接口状态码异常
    def test_questiontext_specialChars(self):
        ret=question_calc_request("\\\\")
        self.assertTrue(ret[1] == 30004, "full ret:%s" % str(ret))

    def test_questiontext_advancedMath(self):
        ret=question_calc_request("\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1")
        # self.assertTrue(ret[1] == 0, "actural code: %s, msg: %s"%(ret[1], ret[2]))
        self.assertTrue(ret[1] == 30004, "full ret:%s" % str(ret))


    def test_questiontext_longQuestionText(self):
        ret=question_calc_request("\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1"
                                  "%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1%2B\sqrt{x+\frac{1}{x}}-\sqrt{x-\frac{1}{x}},|x| \geq 1")
        # self.assertTrue(ret[1] == 0, "actural code: %s, msg: %s"%(ret[1], ret[2]))
        self.assertTrue(ret[1] == 30004, "full ret:%s" % str(ret))


if __name__ == '__main__':
    full_time_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    suite = unittest.TestSuite()
    suite.addTest(ContractedCalcTestsCollector("test_questiontext_normal"))
    suite.addTest(ContractedCalcTestsCollector("test_questiontext_blank"))
    suite.addTest(ContractedCalcTestsCollector("test_questiontext_specialChars"))
    suite.addTest(ContractedCalcTestsCollector("test_questiontext_advancedMath"))
    suite.addTest(ContractedCalcTestsCollector("test_questiontext_longQuestionText"))
    # 实践中发现执行时的当前路径，不一定是此文件所在的文件夹，所以使用绝对路径
    print(f"{os.getcwd()}")
    filename = './result/html/ContractedCalcTestsCollector_%s.html' % full_time_timestamp
    fb = open(filename, 'wb+')
    runner = HTMLTestRunner(stream=fb, title="ContractedCalcTestsCollector Report", description="test")
    runner.run(suite)
    fb.close()