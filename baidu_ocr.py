import glob
import itertools
import os
import config as cfg

from aip import AipOcr

"""
https://console.bce.baidu.com/ai/#/ai/ocr/app/detail~appId=1747453
 pip install baidu-aip -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
FLAGS = cfg.FLAGS


class BaiduOcr(object):
    def __init__(self):
        self.APP_ID = cfg.APP_ID
        self.API_KEY = cfg.API_KEY
        self.SECRET_KEY = cfg.SECRET_KEY
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def gen_text(self, filepath):
        image = self.get_file_content(filepath)
        text = self.client.basicGeneral(image)
        try:
            words_result = text['words_result']
        except:
            words_result = []
        texts = [i['words'] for i in words_result]
        texts = "".join(itertools.chain(*texts))  # 将一维列表变成一个字符串
        return texts

    def judge_card_baidu(self, filePath):
        """
        判断一张图片的类别
        :param flag:
        :param filePath:
        :return:
        """
        texts = self.gen_text(filePath)
        flags = FLAGS
        for num, flag in enumerate(flags):
            if flag in texts:
                return flag

        return None




# ocr = BaiduOcr()
# ocr.judge_card("/home/huangjx/Projects/Thursday_yolo3/bank_logo/ZS800_FH18082408.jpg")
# # ocr.judge_card_dir('../bank_logo')