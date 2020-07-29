import glob
import itertools
import os
import shutil

import cv2
import numpy as np
from PIL import Image
from ..mp4func.mp4func import Mp4Func  # 采取了相对导入方式，这份脚本不能作为启动文件


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
        ref_son123 = ref[0:3 * int(h / 4), :, :]
        ref_son12345 = ref[0:5 * int(h / 6), :, :]
        imgs = {
            'ref_son1': ref_son1,
            'ref_son2': ref_son2,
            'ref_son3': ref_son3,
            'ref_son4': ref_son4,
            'ref': ref,
            'ref_son123': ref_son123,
            'ref_son12345': ref_son12345,
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

    def write_wenzi(self, wenzis, wenzi_path):
        """
        以“附加文件”的形式将文字写入文档
        :param wenzi: 文字或者是包含很多文字的列表
        :param wenzi_path: 保存文件
        :return:
        """
        if isinstance(wenzis, list):
            for i, wenzi in enumerate(wenzis):
                with open(wenzi_path, 'a') as f:
                    f.write(wenzi + '\n')
        else:
            with open(wenzi_path, 'a') as f:
                f.write(wenzis + '\n')

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
        (核心代码)
        对图片进行预处理之后识别出图片上所有可能的文字
        :param jpg: 图片路径
        :return: 该图片识别到的可能所有文字
        """
        imgs = self.jpg_cut(jpg)  # 图片切分
        imgs = self.channel(imgs['ref_son12345'])  # 选取整张图片除了底下说明部分，对图片进行颜色通道变换
        wenzis = ''
        for i, img in imgs.items():
            img = self.np_to_bin(img)
            if self.baidu is not None:
                wenzi = self.baidu.ocr(binary_content=img)
                wenzis += wenzi
            if self.fs is not None and (i % 2) == 0:
                wenzi = self.fs.ocr(binary_content=img)
                wenzis += wenzi

        # return self.not_repeat(wenzis)
        return wenzis  # 不进行去重，宁愿多一点信息也比少一点信息好判断

    def mp4_indentify(self, mp4_path, frame_path):
        """
        将视频识别出的所有可能文字写在文档里面
        :param mp4_path: 视频路径
        :param frame_path: 帧路径
        :return: 返回True
        """
        mp4func = Mp4Func()
        frame_path = mp4func.get_frame_from_mp4(mp4_path, frame_path)
        BaseName = os.path.abspath(frame_path)
        jpgs = sorted(glob.glob(os.path.join(BaseName, "*.jpg")))  # 读取文件夹下面所有的文件,并排序
        wenzis = []
        try:
            for i, jpg in enumerate(jpgs):
                # print(jpg)  # 测试阶段在终端显示代码
                wenzi = self.jpg_indentify(jpg)
                wenzis.append(wenzi)
            return wenzis
        except:
            return wenzis

    def add_sensitive_works(self, sensitive):
        pass

    def classify(self, sensitive_works, wenzi=None, wenzis=None, wenzifile=None):
        """
        判断是否出现敏感词，出现的个数有多少
        :param sensitive_works:
        :param wenzi: 文字字符串
        :param wenzis: 文字字符串列表
        :param wenzifile: 文字字符串文件
        :return: 包含所有可能的敏感词
        """
        all_probably_sensitive_works = []
        if wenzi is not None:
            for i, work in enumerate(sensitive_works):
                if work in wenzi:
                    all_probably_sensitive_works.append(work)
        elif wenzis is not None:
            wenzis = "".join(itertools.chain(*wenzis))  # 将一维列表变成一个字符串
            for i, work in enumerate(sensitive_works):
                if work in wenzis:
                    all_probably_sensitive_works.append(work)
        elif wenzifile is not None:
            with open(wenzifile) as f:
                wenzis = f.readlines()
            wenzis = "".join(itertools.chain(*wenzis))  # 将一维列表变成一个字符串
            for i, work in enumerate(sensitive_works):
                if work in wenzis:
                    all_probably_sensitive_works.append(work)
        return all_probably_sensitive_works
