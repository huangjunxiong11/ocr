import glob
import itertools
import os
import config as cfg
from utils.pre import Pre
from aip import AipOcr

"""
https://console.bce.baidu.com/ai/#/ai/ocr/app/detail~appId=1747453
 pip install baidu-aip -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
FLAGS = cfg.FLAGS
pre = Pre()


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

    def get_card_text(self, filepath):
        image = self.get_file_content(filepath)
        text = self.client.bankcard(image)  # 识别银行卡
        try:
            words_result = text['result']
            texts = words_result['bank_name']
            texts = "".join(itertools.chain(*texts))
        except:
            texts = []
        return texts

    def from_bin(self, img_bin):
        text = self.client.basicGeneral(img_bin)
        try:
            words_result = text['words_result']
        except:
            words_result = []
        texts = [i['words'] for i in words_result]
        texts = "".join(itertools.chain(*texts))  # 将一维列表变成一个字符串
        return texts

    def get_dir(self, dir):
        bash_dir = os.path.abspath(dir)
        images = []
        images += glob.glob(os.path.join(bash_dir, '*.png'))
        images += glob.glob(os.path.join(bash_dir, '*.jpg'))
        images += glob.glob(os.path.join(bash_dir, '*.jpeg'))

        return images

    def get_four_text(self, filename):
        texts = []
        ab = pre.four_cut(filename)
        for i, j in enumerate(ab):
            text = ocr.from_bin(j)
            texts.append(text)
        pass
        texts = "".join(itertools.chain(*texts))  # 将一维列表变成一个字符串
        return texts


if __name__ == '__main__':

    ocr = BaiduOcr()
    # pre = Pre()
    #
    # dir = "/home/huangjx/Projects/git-pro/ocr/银行卡/浦发银行-字体限制"
    # images = ocr.get_dir(dir)
    # for m, n in enumerate(images):
    #     # print(n)
    #     ab = pre.four_cut(n)
    #     for i, j in enumerate(ab):
    #         text = ocr.from_bin(j)
    #         if '浦发' in text:
    #             print(n)
    #             break

    # n = "/home/huangjx/Projects/git-pro/ocr/银行卡/浦发银行-字体限制/吉利.png"
    # ab = pre.four_cut(n)
    # for i, j in enumerate(ab):
    #     text = ocr.from_bin(j)
    #     if '浦发' in text:
    #         print(n)
    #         break

    # ocr.gen_text('/home/huangjx/Projects/git-pro/ocr/ref_son1.png')

    ocr.get_four_text("/home/huangjx/Projects/git-pro/ocr/银行卡/浦发银行-字体限制/吉利.png")
    pass