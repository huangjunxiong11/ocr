import glob
import os
import cv2
import numpy as np
from PIL import Image
from ..mp4func.mp4func import Mp4Func


class Identify(object):
    def __init__(self, baidu=None, fs=None, db=None):
        self.baidu = baidu
        self.fs = fs
        self.db = db
        pass

    def jpg_cut(self, jpg):
        """
        将图片平均切分为四份
        :param jpg: 本地图片路径
        :return: 返回四份数组
        """
        ref = cv2.imread(filename=jpg)
        h, w, c = ref.shape
        ref_son1 = ref[0:int(h / 4), :, :]
        ref_son2 = ref[int(h / 4):int(h / 2), :, :]
        ref_son3 = ref[int(h / 2):3 * int(h / 4), :, :]
        ref_son4 = ref[3 * int(h / 4):h, :, :]
        imgs = {
            'ref_son1': ref_son1,
            'ref_son2': ref_son2,
            'ref_son3': ref_son3,
            'ref_son4': ref_son4,
            'ref': ref,
        }
        return imgs

    def channel(self, np_imgs):
        """
        改变图片通道位置，以此来改变字体颜色
        :param np_imgs: 原始图片数组
        :return: 字典
        """
        b, g, r = cv2.split(np_imgs)

        bgr = cv2.merge([b, g, r])
        brg = cv2.merge([b, r, g])
        gbr = cv2.merge([g, b, r])

        grb = cv2.merge([g, r, b])
        rbg = cv2.merge([r, b, g])
        rgb = cv2.merge([r, g, b])

        imgs = {
            'bgr': bgr,
            'brg': brg,
            'gbr': gbr,
            'grb': grb,
            'rbg': rbg,
            'rgb': rgb,
        }
        return imgs

    def np_to_bin(self, np_data):
        """
        将图片数组变成二进制
        :param np_data: 图片数组
        :return: 二进制
        """
        ret, buf = cv2.imencode(".jpg", np_data)
        img_bin = Image.fromarray(np.uint8(buf)).tobytes()
        return img_bin

    def write_wenzi(self, wenzi, wenzi_path):
        """
        以“附加文件”的形式将文字写入文档
        :param wenzi: 文字
        :param wenzi_path: 保存文件
        :return:
        """
        with open(wenzi_path, 'a') as f:
            f.write(wenzi + '\n')

    def not_repeat(self, strs):
        """
        给文字字符串去重
        :param strs:
        :return:
        """
        text = ""
        for i in strs:
            if i not in text:
                text += i

        return text

    def jpg_indentify(self, jpg):
        """
        对图片进行预处理之后识别出图片上所有可能的文字
        :param jpg: 图片路径
        :return: 该图片识别到的可能所有文字
        """
        imgs = self.jpg_cut(jpg)
        # imgs = self.channel(imgs['ref_son3'])  # 只挑选包含字幕的图片部分
        imgs = self.channel(imgs['ref'])  # 选取整张图片
        wenzis = ''
        for i, img in imgs.items():
            img = self.np_to_bin(img)
            if self.baidu is not None:
                wenzi = self.baidu.get_text(bins=img)
                wenzis += wenzi
            if self.fs is not None:
                wenzi = self.fs.ocr(binary_content=img)
                wenzis += wenzi

        return self.not_repeat(wenzis)

    def mp4_indentify(self, mp4_path, frame_path, sensitive_words):
        frame_path = Mp4Func.get_frame_from_mp4(mp4_path, frame_path)
        BaseName = os.path.abspath(frame_path)
        jpgs = glob.glob(os.path.join(BaseName, "*.jpg"))  # 读取文件夹下面所有的文件
        for i, jpg in enumerate(jpgs):
            flag = self.jpg_indentify(jpg)
        pass
