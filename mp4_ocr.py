import glob
import os
from moviepy.editor import *
from baidu_ocr import BaiduOcr
from ocr_tool import OcrTool
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64


class Mp4Pre(object):
    def __init__(self):

        self.baidu = BaiduOcr()
        self.ocr_tool = OcrTool(ocr_docker_url='http://192.168.8.126:5010')
        pass

    def np_to_bin(self, np_data):
        """
        将图片数组编码成二进制
        :param np_data:
        :return:
        """
        ret, buf = cv2.imencode(".jpg", np_data)
        img_bin = Image.fromarray(np.uint8(buf)).tobytes()
        return img_bin

    def file_to_bin(self, filePath):
        """
        将图片文件读取成二进制
        :param filePath:
        :return:
        """

        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_34_bins(self, filename):
        """
        输出一张图片名字，输出这张图片4分之3位置图片的彩色和灰白二进制数值列表
        :param filename:
        :return:[np_bin3, file_bin3, gray_np_bin3, gray_file_bin3]
        """
        rgb_ref = cv2.imread(filename=filename)
        h, w, c = rgb_ref.shape
        ref_son3 = rgb_ref[int(h / 2):3 * int(h / 4), :, :]
        np_bin3 = self.np_to_bin(ref_son3)
        cv2.imwrite('rgb_ref_son3.png', ref_son3)
        file_bin3 = self.file_to_bin("rgb_ref_son3.png")

        gray_ref = cv2.imread(filename, 0)
        gray_ref = cv2.merge([gray_ref, gray_ref, gray_ref])
        h, w, c = gray_ref.shape
        gray_ref_son3 = gray_ref[int(h / 2):3 * int(h / 4), :, :]
        gray_np_bin3 = self.np_to_bin(gray_ref_son3)
        cv2.imwrite('gray_ref_son3.png', gray_ref_son3)
        gray_file_bin3 = self.file_to_bin("gray_ref_son3.png")

        return [np_bin3, file_bin3, gray_np_bin3, gray_file_bin3]

    def file_texts(self, filename):
        """
        识别切分3/4图片之后的四份不同的二进制数组
        :param filename:
        :return: 返回输入图片中识别出来的所有文字
        """
        imgbins = self.get_34_bins(filename)
        texts = ''
        for imgbin in imgbins:
            t1 = self.baidu.from_bin_to_text(imgbin)
            t2 = self.ocr_tool.ocr_bin_to_text(imgbin)
            texts = texts + t1 + t2
        return texts

    def baidu_texts(self, filename):
        """
        通过百度通用ocrAPI识别图片中的文字
        :param filename:
        :return:返回输入图片中识别出来的所有文字
        """
        texts = self.baidu.gen_text(filename)
        return texts

    def fengshen_texts(self, filename):
        """
        通过fengshen通用ocrAPI识别图片中的文字
        :param filename:
        :return:返回输入图片中识别出来的所有文字
        """
        texts = self.ocr_tool.ocr(filename)
        return texts

    def frame_img_texts(self, filename):
        """
        输出一张图片，输出这张图片中可能包含的所有文字
        :param filename:
        :return:
        """
        # try:
        #     texts1 = self.file_texts(filename)
        # except:
        #     texts1 = ''
        try:
            texts2 = self.fengshen_texts(filename)
        except:
            texts2 = ''
        # try:
        #     texts3 = self.baidu_texts(filename)
        # except:
        #     texts3 = ''
        # texts = texts1 + texts2 + texts3
        texts = texts2
        return texts


class WeiBao(Mp4Pre):
    def __init__(self, frame_path):
        super().__init__()
        self.frame_path = frame_path
        pass

    def from_mp4_get_frame(self, mp4_path):
        """
        输出一个视频，然后将该视频的图片帧给保存下来
        :param mp4_path:
        :param frame_path:
        :return:
        """
        basename = os.path.basename(mp4_path).split('.')[0]
        clip = VideoFileClip(mp4_path)
        if not os.path.exists(basename):
            os.makedirs(basename)
        i = 1
        fps = clip.fps
        for frame in clip.iter_frames():
            if i % fps == 0:
                img = Image.fromarray(frame)
                save_name = os.path.join(basename, "%05d.jpg" % i)
                img.save(save_name)
                # cv2.imwrite(save_name, frame)
                # yield save_name
            i += 1
        return os.path.abspath(basename)

    def img_works_identify(self, filename, sensitive_words):
        """
        输入一张图片，输出这张图片的所有可能文字中是否包含敏感词，如果有包含，返回True
        True表示包含敏感词
        False表示不包含敏感词
        :param filename:
        :return:
        """
        texts = self.frame_img_texts(filename)
        for i, work in enumerate(sensitive_words):
            if work in texts:
                return True
        return False

    def mp4_works_identify(self, sensitive_words):
        """
        输入一个包含frame图片的文件夹，如果某一张图片中存在某些敏感词，则直接返回True，中断循环
        True表示包含敏感词
        False表示不包含敏感词
        :return:
        """
        bash_dir = os.path.abspath(self.frame_path)
        images = []
        # images += glob.glob(os.path.join(bash_dir, '*.png'))
        images += glob.glob(os.path.join(bash_dir, '*.jpg'))
        # images += glob.glob(os.path.join(bash_dir, '*.jpeg'))
        for i, image in enumerate(images):
            # print(image)
            if self.img_works_identify(image, sensitive_words):
                return True
        return False


if __name__ == '__main__':
    # fangaix_sensitive_works = ['医疗险', '百万医疗险', '600万', '1元', '14元', '人保', '中国人保', '售完即止', '再不买就没了']
    # yilx_sensitive_works = ['防癌', '防癌险', '200万', '3元', '4.1元', '人保', '中国人保', '售完即止', '再买就没了']
    # mp4pre = Mp4Pre()
    # name = "/home/huangjx/Projects/git-pro/ocr/data/shu-/00690.jpg"
    # print(mp4pre.file_texts(name))
    # print(mp4pre.baidu_texts(name))
    # print(mp4pre.fengshen_texts(name))
    # weibao = WeiBao('./frame')
    # weibao.from_mp4_get_frame('/home/huangjx/Projects/git-pro/ocr/data/heng.mp4')
    pass
