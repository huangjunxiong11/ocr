import itertools
from aip import AipOcr

"""
https://console.bce.baidu.com/ai/#/ai/ocr/app/detail~appId=1747453
 pip install baidu-aip -i https://pypi.tuna.tsinghua.edu.cn/simple
"""


class BaiduOcr(object):
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def get_file_content(self, filePath):
        """
        :param filePath: 文件路径
        :return: 文件的二进制表示
        """
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_text(self, filepath=None, bins=None):
        """
        输入的是图片路径或者是二进制表示，输出的是该图片上所识别出来的文字，是一个字符串
        :param filepath:图片路径
        :return:该图片上所识别出来的文字，是一个字符串
        """
        try:
            if filepath is not None:
                image = self.get_file_content(filepath)
                text = self.client.basicGeneral(image)
            else:
                text = self.client.basicGeneral(bins)

            words_result = text['words_result']
        except:
            words_result = []
        texts = [i['words'] for i in words_result]
        texts = "".join(itertools.chain(*texts))  # 将一维列表变成一个字符串
        return texts

    def get_card_text(self, filepath):
        """
        输入的是一张图片的路径，输出的是该图片上所识别出来的银行类别文字是一个字符串
        :param filepath:图片的路径
        :return:该图片上所识别出来的银行类别文字是一个字符串
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


if __name__ == '__main__':
    pass
