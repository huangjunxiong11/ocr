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
        """
        输入的是图片路径，输出的是该图片上所识别出来的文字，是一个字符串
        :param filepath:
        :return:
        """
        image = self.get_file_content(filepath)
        # a = image.decode('utf-8')  # 代码出错，参数无效
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
        输入的是一张图片的路径，判断这张图片的所属类别
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
        """
        输入的是一张图片的路径，输出的是该图片上所识别出来的银行类别文字是一个字符串
        :param filepath:
        :return:
        """
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
        """
        输入的是一张图片的二进制表示，输出的是该图片上所识别出来的文字，是一个字符串
        :param img_bin:
        :return:
        """
        text = self.client.basicGeneral(img_bin)
        try:
            words_result = text['words_result']
        except:
            words_result = []
        texts = [i['words'] for i in words_result]
        texts = "".join(itertools.chain(*texts))  # 将一维列表变成一个字符串
        for flag in FLAGS:
            if flag in texts:
                return flag
        return None

    def from_bin_to_text(self, img_bin):
        """
        输入的是一张图片的二进制表示，输出的是该图片上所识别出来的文字，是一个字符串
        :param img_bin:
        :return:
        """
        text = self.client.basicGeneral(img_bin)
        try:
            words_result = text['words_result']
        except:
            words_result = []
        texts = [i['words'] for i in words_result]
        texts = "".join(itertools.chain(*texts))  # 将一维列表变成一个字符串
        return texts

    def get_dir(self, dir):
        """
        输入一个文件夹，输入该文件夹下面包含的所有图片文件的路径
        :param dir:
        :return:
        """
        bash_dir = os.path.abspath(dir)
        images = []
        images += glob.glob(os.path.join(bash_dir, '*.png'))
        images += glob.glob(os.path.join(bash_dir, '*.jpg'))
        images += glob.glob(os.path.join(bash_dir, '*.jpeg'))

        return images

    def get_four_text(self, filename):
        """
        输入一张图片，通过切分四份的方法输出该图片上包含的文字
        :param filename:
        :return:
        """
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
