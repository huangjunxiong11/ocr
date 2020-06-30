# -*- coding: utf-8 -*-
import base64
import itertools

import requests
from flask_jsonrpc.proxy import ServiceProxy
import config as cfg
import os
import glob
from aip import AipOcr


class OcrTool:

    def __init__(self, ocr_docker_url):
        if not str(ocr_docker_url).startswith('http://'):
            ocr_docker_url = 'http://' + ocr_docker_url
        self.service = ServiceProxy('{}/session'.format(ocr_docker_url))

    def img_from_url(self, url):
        r = requests.get(url, timeout=20).content
        return base64.b64encode(r).decode()

    def img_from_path(self, file_path):
        return base64.b64encode(open(file_path, 'rb').read()).decode()

    def ocr(self, file_path=None, url=None, binary_content=None, split_str='<br>'):
        if url is not None:
            img = self.img_from_url(url)
        elif file_path is not None:
            img = self.img_from_path(file_path)
        elif binary_content is not None:
            img = base64.b64encode(binary_content).decode()
        else:
            raise ValueError('You should set url or file_path or binary_content.')

        try:
            response = self.service.ocr(img)
        except:
            print('Error:url is {} , file_path is {}'.format(url, file_path))
            response = list()
        text_list = list()
        try:
            # response有可能出现返回错误值
            for j in response:
                if j['text'] != '':
                    text_list.append(j['text'])
        except:
            text_list = []

        # return '{}'.format(split_str).join(text_list)
        return ''.join(text_list)

    def ocr_list(self, file_path_list=None, url_list=None, binary_content_list=None, split_str='<br>'):
        img_list = list()
        if url_list is not None:
            for url in url_list:
                img = self.img_from_url(url)
                img_list.append(img)
        elif file_path_list is not None:
            for file_path in file_path_list:
                img = self.img_from_path(file_path)
                img_list.append(img)
        elif binary_content_list is not None:
            for binary_content in binary_content_list:
                img = base64.b64encode(binary_content).decode()
                img_list.append(img)
        else:
            raise ValueError('You should set url or file_path or binary_content.')

        response_list = self.service.ocr_list(img_list)

        obj = list()
        for response in response_list:
            text_list = list()
            for j in response:
                if j['text'] != '':
                    text_list.append(j['text'])
            obj.append('{}'.format(split_str).join(text_list))
        return obj

    def ocr_video(self, url=None, binary_content=None):
        r = self.service.ocr_video(url=url, binary_content=binary_content)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])
        return r

    def speech_video(self, url=None, binary_content=None):
        r = self.service.speech_video(url=url, binary_content=binary_content)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])
        return r

    def video_append(self, image_content, movie_content, download_path=None, cover_position='first', cover_hold_sec=2):
        print('开始执行视频添加图片首帧（尾帧）功能，正在执行中...')
        r = self.service.video_append(image_content=image_content,
                                      movie_content=movie_content, cover_position=cover_position,
                                      cover_hold_sec=cover_hold_sec)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        if download_path is not None:
            with open(download_path, 'wb') as f:
                f.write(base64.b64decode(r))
        print('添加图片首帧（尾帧）执行成功')
        return r

    def video_resize(self, movie_content, percent=None, resize=None, download_path=None):
        """

        :param movie_content: [bytes] 视频二进制流
        :param percent: [float]放缩比例，按0.5倍数相乘
        :param resize: [tuple](width,height)
        :param download_path: [str] 下载路径
        :return: [bytes] 返回的视频二进制流
        """
        print('开始执行视频等比例修改尺寸功能，正在执行中..')

        r = self.service.video_resize(movie_content=movie_content, percent=percent, resize=resize)

        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        if download_path is not None:
            with open(download_path, 'wb') as f:
                f.write(base64.b64decode(r))
        print('视频等比例修改尺寸功能执行成功')
        return r

    def get_video_size(self, movie_content):
        r = self.service.get_video_size(movie_content=movie_content)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        return r

    def sr_picture(self, img_content, multiple=2, download_path=None):
        r = self.service.sr_picture(img_content=img_content, multiple=multiple)
        if isinstance(r, dict) and 'error' in r.keys():
            raise ValueError(r['error']['stack'])

        if download_path is not None:
            with open(download_path, 'wb') as f:
                f.write(base64.b64decode(r))
        return r


class Judge(OcrTool):
    def __init__(self, url=cfg.URL):
        super(Judge, self).__init__(ocr_docker_url=url)

    def judge_card(self, filepath):
        texts = self.ocr(file_path=filepath)
        # baidu = BaiduOcr()
        # texts_baidu = baidu.gen_text(filePath=filepath)
        # texts = texts + texts_baidu
        flags = cfg.FLAGS
        for num, flag in enumerate(flags):
            if flag in texts:
                return flag
        return None



if __name__ == '__main__':
    # 示例
    object = Judge()
    # object.judeg_card_dir('_bank_logo')
    object.judge_card('/home/huangjx/Projects/git-pro/ocr/ref_son1.png')
    """
    注意：所有图片位于文件夹data下面
    """
# 自信一点,你的优点呢?
# 你想要一个什么样的生活?
# 她的生活跟你的生活差别太大了,觉得自己不配?你是不是觉得自己不配?
# 你能付出什么?她想要什么?
# 如何挣钱?我是不是飘了
# 你想要被自己喜欢的人爱?所以你苦苦追寻,你要不要先去学着爱自己?就是说,如果你就是那个可能喜欢自己的人,你会喜欢现在的自己吗?
# 如果你要爱自己,你如何去爱自己呢?做自己喜欢做的事情,给自己买自己喜欢的东西,让自己变好看,不再去想着未来能不能娶到老婆,
# 如果未来我娶不到老婆,我还有自己永远不会离开自己的人,就是自己.我会永远爱着自己,会永远做着自己喜欢做的事情,永远让自己长得好看,
# 那我对所谓的未来还有任何其它恐惧吗?对的,我要先学会去爱自己,做自己喜欢的事情,我一直都做着自己喜欢的事情,每个月的工资留不留也无所谓了.
# 如果你都不爱自己,谁会来爱你?
